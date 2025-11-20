"""
I (Quentin Desmet) once made this script for converting ``.mdv`` files (ARM)
to ``.nc``. It may not work if you run it directly, but it may simply be an
inspiration.

Note that you need `Py-ART <https://arm-doe.github.io/pyart/>`_
(I downloaded and installed it directly from github).
"""

from datetime import datetime
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pyart
import xarray as xr


def mdv_to_dataset(path: Path) -> xr.Dataset:
    """
    Return the mdv-formatted data in ``path`` as an xarray Dataset.
    """

    def get_attrs(d: dict, **kwargs) -> dict:
        """Remove 'data' from the items in ``d`` and update with ``kwargs``."""
        res = {k: v for k, v in d.items() if k != "data"}
        res.update(kwargs)
        return res

    def process_categorical(d: dict) -> Tuple[np.ndarray, dict]:
        """
        Check whether 'data' contains categorical strings, convert to int if needed.
        """

        def char_to_categorical(
            a: np.ndarray, comment: str, name: str = ""
        ) -> Tuple[np.ndarray, str]:
            """Turn a char array into categorical using integers."""
            # Parse comment
            parts = comment.split(".")
            option_list = parts[0]
            if len(parts) > 1:
                end = ("." + ".".join([p for p in parts[1:]])).replace('"', "'")
            else:
                end = ""

            options = option_list.split(": ")[1].strip().strip('"').split('", "')
            option_to_index = {o: i + 1 for i, o in enumerate(options)}

            # Convert array
            def f_oti(o: str) -> int:
                """Embed function to map string options to corresponding integers."""
                try:
                    return option_to_index[o.decode("utf-8")]
                except KeyError as e:
                    raise ValueError(
                        f"Option '{o}' is not listed in the 'comment' attribute"
                        + (f" for variable '{name}'" if name else "")
                        + "."
                    )

            res = np.array(list(map(f_oti, a)))

            # Rewrite comment
            equiv = (
                option_list.split(": ")[0]
                + ": "
                + ", ".join([f"'{o}' ({i})" for o, i in option_to_index.items()])
                + end
            )

            return res, equiv

        data = d["data"]
        attrs = get_attrs(d)

        if data.dtype.kind in "STU":
            try:
                com_key = "comment"
                comment = attrs[com_key]
                assert "comments" not in attrs.keys()
            except KeyError:
                try:
                    com_key = "comments"
                    comment = attrs[com_key]
                except Exception:
                    raise

            data, comment = char_to_categorical(data, comment, name=attrs["long_name"])
            attrs.update({com_key: comment})

        return data, attrs

    # Read
    radar = pyart.io.read_mdv(path)
    time = datetime.strptime(
        f"{path.parent.name} {path.with_suffix('').name}", "%Y%m%d %H%M%S"
    )

    # Check
    assert radar.ngates == len(radar.range["data"])
    assert radar.nrays == len(radar.time["data"])
    assert radar.nrays == len(radar.elevation["data"])
    assert radar.nrays == len(radar.azimuth["data"])
    assert radar.nsweeps == len(radar.sweep_number["data"])
    assert radar.nrays % radar.nsweeps == 0
    nangles = radar.nrays // radar.nsweeps

    # Reshape
    r = radar.elevation["data"].reshape(radar.nsweeps, nangles)
    assert np.all(r[:, 1:] == r[:, 0:1])
    del r
    elevation = radar.elevation["data"][::nangles]
    r = radar.azimuth["data"].reshape(radar.nsweeps, nangles)
    assert np.all(r[0:1] == r[1:])
    del r
    azimuth = radar.azimuth["data"][:nangles]
    ray_time = radar.time["data"].reshape(radar.nsweeps, nangles)

    # Coordinates
    coords = {
        k: xr.DataArray(
            getattr(radar, k)["data"],
            name=k,
            dims=[k],
            attrs=get_attrs(getattr(radar, k)),
        )
        for k in ["longitude", "latitude", "altitude", "range"]
    }
    coords["time"] = xr.DataArray(
        np.array([time]),
        name="time",
        dims=["time"],
        attrs=dict(standard_name="time", long_name="time"),
    )
    coords["elevation"] = xr.DataArray(
        elevation,
        name="elevation",
        dims=["elevation"],
        attrs=get_attrs(radar.elevation),
    )
    coords["azimuth"] = xr.DataArray(
        azimuth, name="azimuth", dims=["azimuth"], attrs=get_attrs(radar.azimuth)
    )
    coords["ray_time"] = xr.DataArray(
        ray_time,
        name="ray_time",
        dims=["elevation", "azimuth"],
        attrs=get_attrs(radar.time, standard_name="ray_time"),
    )

    # Attributes
    attrs = radar.metadata

    history = attrs.get("history", "")
    history += (
        ("; " if history else "")
        + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        + ": Read from mdv to xarray Dataset"
    )
    attrs.update(dict(history=history))

    for k in [
        "scan_type",
    ]:
        attrs[k] = getattr(radar, k)

    if isinstance(radar.projection, str):
        attrs["proj"] = radar.projection
    else:
        assert isinstance(radar.projection, dict)
        attrs.update(
            {
                k if k == "proj" else f"proj{k}": str(v)
                for k, v in radar.projection.items()
            }
        )

    for k in [
        "target_scan_rate",
        "rays_are_indexed",
        "ray_angle_res",
        "scan_rate",
        "antenna_transition",
        "rotation",
        "tilt",
        "roll",
        "drift",
        "heading",
        "pitch",
        "georefs_applied",
        "radar_calibration",
    ]:
        if getattr(radar, k) is not None:
            raise ValueError(f"Processing stream for {k} not wired.")

    # Initiate dataset
    ds = xr.Dataset(coords=coords, attrs=attrs)

    # Variables
    for k, v in radar.fields.items():
        ds = ds.assign(
            {
                k: xr.DataArray(
                    v["data"].reshape(1, radar.nsweeps, -1, radar.ngates),
                    name=k,
                    dims=["time", "elevation", "azimuth", "range"],
                    attrs=get_attrs(v),
                )
            }
        )

    for k in [
        "gate_z",
        "gate_latitude",
        "gate_altitude",
    ]:
        ds = ds.assign(
            {
                k: xr.DataArray(
                    getattr(radar, k)["data"].reshape(
                        1, radar.nsweeps, -1, radar.ngates
                    ),
                    name=k,
                    dims=["time", "elevation", "azimuth", "range"],
                    attrs=get_attrs(getattr(radar, k)),
                )
            }
        )

    for k in [
        "sweep_number",
        "sweep_mode",
        "fixed_angle",
        "sweep_start_ray_index",
        "sweep_end_ray_index",
        "rays_per_sweep",
    ]:
        array, attrs = process_categorical(getattr(radar, k))
        ds = ds.assign(
            {
                k: xr.DataArray(
                    array,
                    name=k,
                    dims=["elevation"],
                    attrs=attrs,
                )
            }
        )

    for k, v in radar.instrument_parameters.items():
        array, attrs = process_categorical(v)

        if len(array) == 1:
            r = array
            dims = ["time"]
        elif len(array) == radar.nsweeps:
            r = array.reshape(1, -1)
            dims = ["time", "elevation"]
        elif len(array) == radar.nrays:
            r = array.reshape(1, radar.nsweeps, -1)
            dims = ["time", "elevation", "azimuth"]
        else:
            raise ValueError(
                f"Unsupported array format for instrument parameter {k}: {len(array)}"
            )

        ds = ds.assign(
            {
                k: xr.DataArray(
                    r,
                    name=k,
                    dims=dims,
                    attrs=attrs,
                )
            }
        )

    return ds


def optimize(
    ds: xr.Dataset, safety_factor: float = 1.0, exclude: List[str] = []
) -> xr.Dataset:
    """Automatically optimize NetCDF storage by scale/offset or integer downcast.

    Parameters
    ----------
    ds
        Input dataset.
    safety_factor
        < 1.0 keeps more precision in scale_factor for floats. Default is 1.0.
    exclude
        Variable names to skip. Default is an empty list.

    Returns
    -------
    packed : xr.Dataset
        Dataset ready for `.to_netcdf()`
    """
    packed = xr.Dataset()
    info = {}

    for var in ds.data_vars:
        if var in exclude:
            packed[var] = ds[var]
            continue

        data = ds[var]
        dtype = data.dtype

        # Floats: apply scale/offset and pack to int
        if np.issubdtype(dtype, np.floating):
            vmin, vmax = np.nanmin(data), np.nanmax(data)
            if not np.isfinite([vmin, vmax]).all():
                packed[var] = data
                continue

            # Try different integer targets from smallest to largest
            for target in [np.int8, np.int16, np.int32]:
                itype = np.iinfo(target)
                scale = (vmax - vmin) / (itype.max - itype.min)
                scale *= safety_factor
                offset = vmin - itype.min * scale
                if np.isfinite(scale) and scale > 0:
                    dtype_final = target
                    break
                else:
                    dtype_final = np.int32  # fallback

            packed_data = np.round((data - offset) / scale).astype(dtype_final)
            packed[var] = xr.DataArray(
                packed_data,
                dims=data.dims,
                coords=data.coords,
                attrs={
                    **data.attrs,
                    "scale_factor": scale,
                    "add_offset": offset,
                    "_FillValue": np.iinfo(dtype_final).min,
                },
            )

        # Integers: try safe downcast
        elif np.issubdtype(dtype, np.signedinteger):
            vmin, vmax = data.min().item(), data.max().item()
            for target in [np.int8, np.int16, np.int32]:
                itype = np.iinfo(target)
                if vmin >= itype.min and vmax <= itype.max:
                    dtype_final = target
                    break
            else:
                dtype_final = dtype

            packed[var] = data.astype(dtype_final)

        # Others: leave untouched
        else:
            packed[var] = data

    packed = packed.assign_coords(**ds.coords)
    packed.attrs.update(ds.attrs)
    return packed


if __name__ == "__main__":

    path_in = Path(
        "/mnt/nfs/d50/tropics/user/desmetq/NO_SAVE/ARM/I1/sur/20110906/202400.mdv"
        # "/mnt/nfs/d50/tropics/user/desmetq/NO_SAVE/ARM/I10/sur/20110819/054310.mdv"
        # "/mnt/nfs/d50/tropics/user/desmetq/NO_SAVE/ARM/I10/vert/20110817/130231.mdv"
    )
    path_out = Path("./test_sur.nc")
    path_out_opt = Path("./test_opt.nc")

    ds = mdv_to_dataset(path_in)
    optimize(ds).to_netcdf(path_out_opt)  # /!\ May induce data precision loss!
    ds.to_netcdf(path_out)

    print(
        f"Size mdv vs netcdf vs netcdf_opt: {float(path_in.stat().st_size) / 1096**2} MB "
        + f"vs {float(path_out.stat().st_size) / 1096**2} MB"
        + f"vs {float(path_out_opt.stat().st_size) / 1096**2} MB"
    )
