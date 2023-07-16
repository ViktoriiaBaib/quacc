"""Slab recipes for EMT"""
from __future__ import annotations

import covalent as ct
from ase import Atoms

from quacc.recipes.emt.core import relax_job, static_job
from quacc.schemas.ase import OptSchema, RunSchema
from quacc.util.slabs import make_max_slabs_from_bulk


def bulk_to_slabs_flow(
    atoms: Atoms | dict,
    make_slabs_kwargs: dict | None = None,
    slab_relax: ct.electron = relax_job,
    slab_static: ct.electron | None = static_job,
    slab_relax_kwargs: dict | None = None,
    slab_static_kwargs: dict | None = None,
) -> list[RunSchema | OptSchema]:
    """
    Workflow consisting of:

    1. Slab generation

    2. Slab relaxations

    3. Slab statics (optional)

    Parameters
    ----------
    atoms
        Atoms object or a dictionary with the key "atoms" and an Atoms object as the value
    make_slabs_kwargs
        Additional keyword arguments to pass to make_max_slabs_from_bulk()
    slab_relax
        Default Electron to use for the relaxation of the slab structures.
    slab_static
        Default Electron to use for the static calculation of the slab structures.
    slab_relax_kwargs
        Additional keyword arguments to pass to the relaxation calculation.
    slab_static_kwargs
        Additional keyword arguments to pass to the static calculation.

    Returns
    -------
    list[dict]
        List of dictionary of results from quacc.schemas.ase.summarize_run or quacc.schemas.ase.summarize_opt_run
    """
    atoms = atoms if isinstance(atoms, Atoms) else atoms["atoms"]
    slab_relax_kwargs = slab_relax_kwargs or {}
    slab_static_kwargs = slab_static_kwargs or {}
    make_slabs_kwargs = make_slabs_kwargs or {}

    if "relax_cell" not in slab_relax_kwargs:
        slab_relax_kwargs["relax_cell"] = False

    @ct.electron
    @ct.lattice
    def _relax_distributed(slabs):
        return [slab_relax(slab, **slab_relax_kwargs) for slab in slabs]

    @ct.electron
    @ct.lattice
    def _relax_and_static_distributed(slabs):
        return [
            slab_static(
                slab_relax(slab, **slab_relax_kwargs),
                **slab_static_kwargs,
            )
            for slab in slabs
        ]

    slabs = ct.electron(make_max_slabs_from_bulk)(atoms, **make_slabs_kwargs)

    if slab_static is None:
        return _relax_distributed(slabs)

    return _relax_and_static_distributed(slabs)