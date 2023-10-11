import pytest
from ase.build import bulk, molecule

from quacc import SETTINGS

pytestmark = pytest.mark.skipif(
    SETTINGS.WORKFLOW_ENGINE != "local",
    reason="Need to use local as workflow manager to run this test.",
)


def test_static_job(tmpdir):
    from quacc.recipes.vasp.core import static_job

    tmpdir.chdir()

    atoms = bulk("Cu") * (2, 2, 2)

    output = static_job(atoms)
    assert output["nsites"] == len(atoms)
    assert "isym" not in output["parameters"]
    assert output["parameters"]["nsw"] == 0
    assert output["parameters"]["lwave"] is True
    assert output["parameters"]["encut"] == 520

    output = static_job(atoms, calc_swaps={"ncore": 2, "kpar": 4})
    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["ncore"] == 2
    assert output["parameters"]["kpar"] == 4

    output = static_job(
        atoms, preset="QMOFSet", calc_swaps={"ismear": 0, "sigma": 0.01, "nedos": None}
    )
    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["ismear"] == -5
    assert output["parameters"]["sigma"] == 0.01

    output = static_job(atoms, calc_swaps={"lwave": None})
    assert "lwave" not in output["parameters"]


def test_relax_job(tmpdir):
    from quacc.recipes.vasp.core import relax_job

    tmpdir.chdir()

    atoms = bulk("Cu") * (2, 2, 2)

    output = relax_job(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["isif"] == 3
    assert output["parameters"]["lwave"] is False
    assert output["parameters"]["encut"] == 520

    output = relax_job(atoms, calc_swaps={"nelmin": 6})
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["isif"] == 3
    assert output["parameters"]["lwave"] is False
    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["nelmin"] == 6

    output = relax_job(atoms, relax_cell=False)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["lwave"] is False
    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["isif"] == 2


def test_doublerelax_job(tmpdir):
    from quacc.recipes.vasp.core import double_relax_job

    tmpdir.chdir()

    atoms = bulk("Cu") * (2, 2, 2)

    output = double_relax_job(atoms)
    assert output["relax1"]["nsites"] == len(atoms)
    assert output["relax1"]["parameters"]["isym"] == 0
    assert output["relax1"]["parameters"]["nsw"] > 0
    assert output["relax1"]["parameters"]["isif"] == 3
    assert output["relax1"]["parameters"]["lwave"] is False
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["isif"] == 3
    assert output["parameters"]["lwave"] is False
    assert output["relax1"]["parameters"]["encut"] == 520
    assert output["parameters"]["encut"] == 520

    output = double_relax_job(atoms, calc_swaps2={"nelmin": 6})
    assert output["relax1"]["nsites"] == len(atoms)
    assert output["relax1"]["parameters"]["isym"] == 0
    assert output["relax1"]["parameters"]["nsw"] > 0
    assert output["relax1"]["parameters"]["isif"] == 3
    assert output["relax1"]["parameters"]["lwave"] is False
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["isif"] == 3
    assert output["parameters"]["lwave"] is False
    assert output["relax1"]["parameters"]["encut"] == 520
    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["nelmin"] == 6

    output = double_relax_job(atoms, relax_cell=False)
    assert output["relax1"]["nsites"] == len(atoms)
    assert output["relax1"]["parameters"]["isym"] == 0
    assert output["relax1"]["parameters"]["nsw"] > 0
    assert output["relax1"]["parameters"]["lwave"] is False
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["lwave"] is False
    assert output["relax1"]["parameters"]["encut"] == 520
    assert output["parameters"]["encut"] == 520
    assert output["relax1"]["parameters"]["isif"] == 2
    assert output["parameters"]["isif"] == 2

    double_relax_job(atoms, calc_swaps1={"kpts": [1, 1, 1]})


def test_slab_static_job(tmpdir):
    from quacc.recipes.vasp.slabs import slab_static_job

    tmpdir.chdir()

    atoms = bulk("Cu") * (2, 2, 2)

    output = slab_static_job(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["idipol"] == 3
    assert output["parameters"]["nsw"] == 0
    assert output["parameters"]["lvhar"] is True
    assert output["parameters"]["encut"] == 450

    output = slab_static_job(atoms, calc_swaps={"nelmin": 6})
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["idipol"] == 3
    assert output["parameters"]["nsw"] == 0
    assert output["parameters"]["lvhar"] is True
    assert output["parameters"]["encut"] == 450
    assert output["parameters"]["nelmin"] == 6

    output = slab_static_job(atoms, calc_swaps={"encut": None})
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["idipol"] == 3
    assert output["parameters"]["nsw"] == 0
    assert output["parameters"]["lvhar"] is True
    assert "encut" not in output["parameters"]


def test_slab_relax_job(tmpdir):
    from quacc.recipes.vasp.slabs import slab_relax_job

    tmpdir.chdir()

    atoms = bulk("Cu") * (2, 2, 2)

    output = slab_relax_job(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isif"] == 2
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["lwave"] is False
    assert output["parameters"]["encut"] == 450

    output = slab_relax_job(atoms, calc_swaps={"nelmin": 6})
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["isif"] == 2
    assert output["parameters"]["nsw"] > 0
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["lwave"] is False
    assert output["parameters"]["encut"] == 450
    assert output["parameters"]["nelmin"] == 6


def test_slab_dynamic_jobs(tmpdir):
    from quacc.recipes.vasp.slabs import bulk_to_slabs_flow, slab_to_ads_flow

    tmpdir.chdir()

    atoms = bulk("Cu")

    ### --------- Test bulk_to_slabs_flow --------- ###

    outputs = bulk_to_slabs_flow(atoms, run_static=False)
    assert len(outputs) == 4
    assert outputs[0]["nsites"] == 80
    assert outputs[1]["nsites"] == 96
    assert outputs[2]["nsites"] == 80
    assert outputs[3]["nsites"] == 64
    assert [output["parameters"]["isif"] == 2 for output in outputs]

    outputs = bulk_to_slabs_flow(atoms)
    assert len(outputs) == 4
    assert outputs[0]["nsites"] == 80
    assert outputs[1]["nsites"] == 96
    assert outputs[2]["nsites"] == 80
    assert outputs[3]["nsites"] == 64
    assert [output["parameters"]["nsw"] == 0 for output in outputs]

    outputs = bulk_to_slabs_flow(
        atoms,
        slab_relax_kwargs={"preset": "SlabSet", "calc_swaps": {"nelmin": 6}},
        run_static=False,
    )
    assert len(outputs) == 4
    assert outputs[0]["nsites"] == 80
    assert outputs[1]["nsites"] == 96
    assert outputs[2]["nsites"] == 80
    assert outputs[3]["nsites"] == 64
    assert [output["parameters"]["isif"] == 2 for output in outputs]
    assert [output["parameters"]["nelmin"] == 6 for output in outputs]
    assert [output["parameters"]["encut"] == 450 for output in outputs]

    outputs = bulk_to_slabs_flow(
        atoms,
        slab_static_kwargs={"preset": "SlabSet", "calc_swaps": {"nelmin": 6}},
    )
    assert len(outputs) == 4
    assert outputs[0]["nsites"] == 80
    assert outputs[1]["nsites"] == 96
    assert outputs[2]["nsites"] == 80
    assert outputs[3]["nsites"] == 64
    assert [output["parameters"]["nsw"] == 0 for output in outputs]
    assert [output["parameters"]["nelmin"] == 6 for output in outputs]
    assert [output["parameters"]["encut"] == 450 for output in outputs]

    ### --------- Test slab_to_ads_flow --------- ###
    atoms = outputs[0]["atoms"]
    adsorbate = molecule("H2")

    outputs = slab_to_ads_flow(atoms, adsorbate, run_static=False)

    assert [output["nsites"] == 82 for output in outputs]
    assert [output["parameters"]["isif"] == 2 for output in outputs]

    outputs = slab_to_ads_flow(atoms, adsorbate)
    assert [output["nsites"] == 82 for output in outputs]
    assert [output["parameters"]["nsw"] == 0 for output in outputs]

    outputs = slab_to_ads_flow(
        atoms,
        adsorbate,
        slab_relax_kwargs={"preset": "SlabSet", "calc_swaps": {"nelmin": 6}},
        run_static=False,
    )

    assert [output["nsites"] == 82 for output in outputs]
    assert [output["parameters"]["isif"] == 2 for output in outputs]
    assert [output["parameters"]["nelmin"] == 6 for output in outputs]
    assert [output["parameters"]["encut"] == 450 for output in outputs]

    outputs = slab_to_ads_flow(
        atoms,
        adsorbate,
        slab_static_kwargs={"preset": "SlabSet", "calc_swaps": {"nelmin": 6}},
    )

    assert [output["nsites"] == 82 for output in outputs]
    assert [output["parameters"]["nsw"] == 0 for output in outputs]
    assert [output["parameters"]["nelmin"] == 6 for output in outputs]
    assert [output["parameters"]["encut"] == 450 for output in outputs]

    adsorbate2 = molecule("CH3")
    adsorbate2.set_initial_magnetic_moments([1, 0, 0, 0])
    outputs = slab_to_ads_flow(atoms, adsorbate2)
    assert [output["nsites"] == 84 for output in outputs]
    assert [output["parameters"]["nsw"] == 0 for output in outputs]


def test_qmof(tmpdir):
    from quacc.recipes.vasp.qmof import qmof_relax_job

    tmpdir.chdir()

    atoms = bulk("Cu")
    output = qmof_relax_job(atoms)
    assert output["prerelax_lowacc"]["nsites"] == len(atoms)
    assert output["prerelax_lowacc"]["parameters"]["sigma"] == 0.01
    assert output["prerelax_lowacc"]["parameters"]["isym"] == 0
    assert output["prerelax_lowacc"]["parameters"]["nsw"] == 0
    assert "isif" not in output["prerelax_lowacc"]["parameters"]
    assert "encut" not in output["prerelax_lowacc"]["parameters"]

    assert output["position_relax_lowacc"]["nsites"] == len(atoms)
    assert output["position_relax_lowacc"]["parameters"]["sigma"] == 0.01
    assert output["position_relax_lowacc"]["parameters"]["isym"] == 0
    assert output["position_relax_lowacc"]["parameters"]["nsw"] > 0
    assert output["position_relax_lowacc"]["parameters"]["isif"] == 2
    assert "encut" not in output["prerelax_lowacc"]["parameters"]

    assert output["volume_relax_lowacc"]["nsites"] == len(atoms)
    assert output["volume_relax_lowacc"]["parameters"]["encut"] == 520
    assert output["volume_relax_lowacc"]["parameters"]["sigma"] == 0.01
    assert output["volume_relax_lowacc"]["parameters"]["isym"] == 0
    assert output["volume_relax_lowacc"]["parameters"]["nsw"] > 0
    assert output["volume_relax_lowacc"]["parameters"]["isif"] == 3

    assert output["double_relax"][0]["nsites"] == len(atoms)
    assert output["double_relax"][0]["parameters"]["encut"] == 520
    assert output["double_relax"][0]["parameters"]["sigma"] == 0.01
    assert output["double_relax"][0]["parameters"]["isym"] == 0
    assert output["double_relax"][0]["parameters"]["nsw"] > 0
    assert output["double_relax"][0]["parameters"]["isif"] == 3

    assert output["double_relax"][1]["nsites"] == len(atoms)
    assert output["double_relax"][1]["parameters"]["encut"] == 520
    assert output["double_relax"][1]["parameters"]["isym"] == 0
    assert output["double_relax"][1]["parameters"]["nsw"] > 0
    assert output["double_relax"][1]["parameters"]["isif"] == 3

    assert output["nsites"] == len(atoms)
    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["sigma"] == 0.01
    assert output["parameters"]["isym"] == 0
    assert output["parameters"]["nsw"] == 0
    assert output["parameters"]["laechg"] is True

    output = qmof_relax_job(atoms, run_prerelax=False)
    assert output["prerelax_lowacc"] is None

    output = qmof_relax_job(atoms, preset="BulkSet", calc_swaps={"nelmin": 6})
    assert output["double_relax"][0]["parameters"]["encut"] == 520
    assert output["double_relax"][0]["parameters"]["nelmin"] == 6
    assert output["double_relax"][0]["parameters"]["sigma"] == 0.05

    assert output["double_relax"][1]["parameters"]["encut"] == 520
    assert output["double_relax"][1]["parameters"]["nelmin"] == 6
    assert output["double_relax"][1]["parameters"]["sigma"] == 0.05

    assert output["parameters"]["encut"] == 520
    assert output["parameters"]["nelmin"] == 6
    assert output["parameters"]["sigma"] == 0.05

    output = qmof_relax_job(atoms, relax_cell=False)
    assert "volume-relax" not in output

    assert output["double_relax"][0]["parameters"]["isif"] == 2
    assert output["double_relax"][1]["parameters"]["isif"] == 2

    atoms = bulk("Cu") * (8, 8, 8)
    output = qmof_relax_job(atoms)


def test_mp(tmpdir):
    from quacc.recipes.vasp.mp import mp_prerelax_job, mp_relax_flow, mp_relax_job

    tmpdir.chdir()

    atoms = bulk("Cu")
    output = mp_prerelax_job(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["xc"] == "pbesol"
    assert output["parameters"]["ediffg"] == -0.05
    assert output["parameters"]["encut"] == 680
    assert output["parameters"]["kspacing"] == 0.22
    assert output["parameters"]["ismear"] == 0

    output = mp_relax_job(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["xc"] == "r2scan"
    assert output["parameters"]["ediffg"] == -0.02
    assert output["parameters"]["encut"] == 680
    assert output["parameters"]["kspacing"] == 0.22
    assert output["parameters"]["ismear"] == 0

    output = mp_relax_flow(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["xc"] == "r2scan"
    assert output["parameters"]["ediffg"] == -0.02
    assert output["parameters"]["encut"] == 680
    assert output["parameters"]["ismear"] == 2
    assert output["parameters"]["kspacing"] == 0.22
    assert output["prerelax"]["parameters"]["xc"] == "pbesol"

    atoms = bulk("Fe")
    output = mp_relax_flow(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["xc"] == "r2scan"
    assert output["parameters"]["ediffg"] == -0.02
    assert output["parameters"]["encut"] == 680
    assert output["parameters"]["ismear"] == 1
    assert output["parameters"]["kspacing"] == pytest.approx(0.28329488761304206)

    atoms = molecule("O2")
    atoms.center(vacuum=10)
    atoms.pbc = True
    output = mp_relax_flow(atoms)
    assert output["nsites"] == len(atoms)
    assert output["parameters"]["xc"] == "r2scan"
    assert output["parameters"]["ediffg"] == -0.02
    assert output["parameters"]["encut"] == 680
    assert output["parameters"]["ismear"] == -5
    assert output["parameters"]["kspacing"] == pytest.approx(0.28329488761304206)