""" tests for MetatasDataset """
# pylint: disable=missing-function-docstring,protected-access,unused-argument

import datetime
import glob
import logging
import os

import pandas as pd
import pytest

from metatlas.datastructures import metatlas_dataset as mads
from metatlas.datastructures import metatlas_objects as metob
from metatlas.io import metatlas_get_data_helper_fun as ma_data


def test_metatlas_dataset_build01(metatlas_dataset):
    assert len(metatlas_dataset) == 1
    assert len(metatlas_dataset[0]) == 1
    assert metatlas_dataset[0][0]["identification"].compound[0].inchi_key == "OLXZPDWKRNYJJZ-RRKCRQDMSA-N"
    assert metatlas_dataset[0][0]["data"]["ms1_summary"]["rt_peak"] == 2.2922415733
    assert (
        metatlas_dataset[0][0]["lcmsrun"].experiment
        == "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583"
    )


@pytest.mark.xfail
def test_metatlas_dataset_build02(mocker, atlas, group_with_2_lcmsruns, df_container):
    # need to mock multiprocessing for this to work
    mocker.patch(
        "metatlas.io.metatlas_get_data_helper_fun.df_container_from_metatlas_file", return_value=df_container
    )
    metatlas_dataset = mads.MetatlasDataset(atlas, [group_with_2_lcmsruns], max_cpus=2)
    assert len(metatlas_dataset) == 2
    assert len(metatlas_dataset[0]) == 1


def test_filter_compounds_ms1_notes_remove01(mocker, metatlas_dataset_with_2_cids, compound):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    metatlas_dataset = metatlas_dataset_with_2_cids
    metatlas_dataset.filter_compounds_ms1_notes_remove()
    assert len(metatlas_dataset[0]) == 2
    metatlas_dataset.set_note(1, "ms1_notes", "Remove")
    metatlas_dataset.filter_compounds_ms1_notes_remove()
    assert len(metatlas_dataset[0]) == 1


def test_filter_compounds01(metatlas_dataset_with_2_cids):
    # mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    metatlas_dataset = metatlas_dataset_with_2_cids
    metatlas_dataset.filter_compounds(remove_idxs=[])
    assert len(metatlas_dataset[0]) == 2
    metatlas_dataset.filter_compounds(keep_idxs=[0, 1])
    assert len(metatlas_dataset[0]) == 2
    metatlas_dataset.filter_compounds(keep_idxs=[])
    assert len(metatlas_dataset[0]) == 0
    with pytest.raises(ValueError):
        metatlas_dataset.filter_compounds()


def test_filter_compounds02(mocker, metatlas_dataset_with_2_cids, compound):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    metatlas_dataset = metatlas_dataset_with_2_cids
    with pytest.raises(ValueError):
        metatlas_dataset.filter_compounds(keep_idxs=[0], remove_idxs=[1])


def test_filter_compounds03(mocker, metatlas_dataset, compound):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    with pytest.raises(IndexError):
        metatlas_dataset.filter_compounds(keep_idxs=[999])


def test_filter_compounds04(mocker, metatlas_dataset, compound):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    with pytest.raises(IndexError):
        metatlas_dataset.filter_compounds(remove_idxs=[999])


def test_filter_hits_by_atlas01(mocker, metatlas_dataset_with_2_cids, hits, compound):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    hits = metatlas_dataset_with_2_cids.hits
    start_num = len(hits)
    metatlas_dataset_with_2_cids.filter_compounds(keep_idxs=[0])
    assert start_num > len(metatlas_dataset_with_2_cids.hits)
    metatlas_dataset_with_2_cids.filter_compounds(remove_idxs=[0])
    assert len(metatlas_dataset_with_2_cids.hits) == 0


def test_polarity(metatlas_dataset):
    assert metatlas_dataset.polarity == "positive"
    metatlas_dataset.filter_compounds(remove_idxs=[0])
    assert len(metatlas_dataset[0]) == 0
    assert metatlas_dataset.polarity == "positive"


def test_extra_time_setter(metatlas_dataset, hits, mocker):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    metatlas_dataset.hits  # pylint: disable=pointless-statement
    assert metatlas_dataset._hits_valid
    metatlas_dataset.extra_time = 0.3
    assert not metatlas_dataset._hits_valid
    metatlas_dataset.hits  # pylint: disable=pointless-statement
    assert metatlas_dataset._hits_valid


def test_rts01(metatlas_dataset):
    metatlas_dataset.set_rt(0, "rt_min", 9.99)
    assert metatlas_dataset.rts[0].rt_min == 9.99
    assert len(metatlas_dataset.rts) == 1


def test_rts02(metatlas_dataset):
    metatlas_dataset._atlas_df_valid = False
    metatlas_dataset.set_rt(0, "rt_max", 9.99)
    assert metatlas_dataset.rts[0].rt_max == 9.99
    assert len(metatlas_dataset.rts) == 1


def test_rts03(metatlas_dataset, analysis_ids, sqlite):
    metatlas_dataset.set_rt(0, "rt_max", 9.99)
    metob.store(metatlas_dataset.atlas)
    atlas_from_db = metob.retrieve("Atlas", unique_id=metatlas_dataset.atlas.unique_id)[0]
    second_metatlas_dataset = mads.MetatlasDataset(analysis_ids, atlas_from_db)
    assert second_metatlas_dataset.rts[0].rt_max == 9.99
    assert len(second_metatlas_dataset.rts) == 1


def test_set_note01(metatlas_dataset, sqlite):
    metatlas_dataset.set_note(0, "ms2_notes", "Foobar")
    assert metatlas_dataset[0][0]["identification"].ms2_notes == "Foobar"


def test_set_note02(metatlas_dataset):
    metatlas_dataset._atlas_df_valid = False
    metatlas_dataset.set_note(0, "ms1_notes", "keeper")
    assert metatlas_dataset[0][0]["identification"].ms1_notes == "keeper"


def test_compound_indices_marked_remove01(sqlite, metatlas_dataset):
    assert len(metatlas_dataset.compound_indices_marked_remove()) == 0
    metatlas_dataset.set_note(0, "ms1_notes", "REMOVE")
    assert len(metatlas_dataset.compound_indices_marked_remove()) == 1


def test_set_nested01():
    with pytest.raises(ValueError):
        mads._set_nested([], [], 0)


def test_set_nested02(atlas):
    mads._set_nested(atlas, ["compound_identifications", 0, ("compound",), 0, ("inchi_key",)], "FOOBAR")
    assert atlas.compound_identifications[0].compound[0].inchi_key == "FOOBAR"


def test_set_nested03(atlas):
    mads._set_nested(atlas, ["name"], "My Atlas")
    assert atlas.name == "My Atlas"


def test_set_nested04(atlas):
    with pytest.raises(TypeError):
        mads._set_nested(atlas, ["zoop"], None)


def test_set_nested05():
    my_dict = {}
    mads._set_nested(my_dict, ["zoop"], None)
    assert my_dict["zoop"] is None


def test_error_if_bad_idxs():
    data = pd.DataFrame(data={"a": [1, 2], "b": [3, 4]})
    mads._error_if_bad_idxs(data, [0])
    with pytest.raises(IndexError):
        mads._error_if_bad_idxs(data, [2])


def test_is_remove():
    assert not mads._is_remove([])
    assert not mads._is_remove("foobar")
    assert mads._is_remove("Remove")
    assert mads._is_remove("REMOVE AND MORE")


def test_duration_since():
    assert mads._duration_since(datetime.datetime.now()) == "0.00 seconds"


def test_filter_compounds_by_signal01(mocker, metatlas_dataset_with_2_cids, df_container, compound):
    mocker.patch(
        "metatlas.io.metatlas_get_data_helper_fun.df_container_from_metatlas_file", return_value=df_container
    )
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[compound])
    assert len(metatlas_dataset_with_2_cids[0]) == 2
    metatlas_dataset_with_2_cids.filter_compounds_by_signal(73, 2.30e6)
    assert len(metatlas_dataset_with_2_cids[0]) == 1
    metatlas_dataset_with_2_cids.filter_compounds_by_signal(73, 2.36e6)
    assert len(metatlas_dataset_with_2_cids[0]) == 0


def test_filter_compounds_by_signal02(mocker, metatlas_dataset_with_2_cids, df_container):
    mocker.patch(
        "metatlas.io.metatlas_get_data_helper_fun.df_container_from_metatlas_file", return_value=df_container
    )
    assert len(metatlas_dataset_with_2_cids[0]) == 2
    metatlas_dataset_with_2_cids.filter_compounds_by_signal(74, 1e5)
    assert len(metatlas_dataset_with_2_cids[0]) == 0


def test_export_atlas_to_csv01(metatlas_dataset, tmp_path):
    out_file = tmp_path / "export.csv"
    metatlas_dataset.export_atlas_to_csv(out_file)
    in_df = pd.read_csv(out_file)
    assert list(in_df.columns) == [
        "Unnamed: 0",
        "chebi_id",
        "chebi_url",
        "creation_time",
        "description",
        "formula",
        "head_id",
        "hmdb_id",
        "hmdb_url",
        "img_abc_id",
        "inchi",
        "inchi_key",
        "iupac_name",
        "kegg_id",
        "kegg_url",
        "last_modified",
        "lipidmaps_id",
        "lipidmaps_url",
        "metacyc_id",
        "mono_isotopic_molecular_weight",
        "name",
        "neutralized_2d_inchi",
        "neutralized_2d_inchi_key",
        "neutralized_inchi",
        "neutralized_inchi_key",
        "num_free_radicals",
        "number_components",
        "permanent_charge",
        "prev_uid",
        "pubchem_compound_id",
        "pubchem_url",
        "source",
        "synonyms",
        "unique_id",
        "username",
        "wikipedia_url",
        "label",
        "id_notes",
        "ms1_notes",
        "ms2_notes",
        "identification_notes",
        "rt_min",
        "rt_max",
        "rt_peak",
        "mz",
        "mz_tolerance",
        "adduct",
        "polarity",
    ]
    assert len(in_df) == 1
    assert in_df.loc[0, "inchi_key"] == "OLXZPDWKRNYJJZ-RRKCRQDMSA-N"


def test_atlas_setter01(metatlas_dataset, atlas_with_2_cids):
    metatlas_dataset.data  # pylint: disable=pointless-statement
    metatlas_dataset.atlas = atlas_with_2_cids
    assert not metatlas_dataset._data_valid
    assert len(metatlas_dataset[0]) == 2


def test_atlas_setter02(metatlas_dataset):
    with pytest.raises(TypeError):
        metatlas_dataset.atlas = [1, 2]


def test_groups01(metatlas_dataset):
    assert metatlas_dataset.groups[0].short_name == "POS_Cone-S1"


def test_set_extra_mz_setter(metatlas_dataset, mocker, hits):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    metatlas_dataset.data  # pylint: disable=pointless-statement
    metatlas_dataset.hits  # pylint: disable=pointless-statement
    metatlas_dataset.extra_mz = 0.43
    assert not metatlas_dataset._data_valid
    assert not metatlas_dataset._hits_valid
    assert metatlas_dataset.extra_mz == 0.43


def test_set_keep_nonmatches_setter(metatlas_dataset, mocker, hits):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    metatlas_dataset.hits  # pylint: disable=pointless-statement
    metatlas_dataset.keep_nonmatches = False
    assert not metatlas_dataset._hits_valid
    assert not metatlas_dataset.keep_nonmatches


def test_set_frag_mz_tolerance_setter(metatlas_dataset, mocker, hits):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    metatlas_dataset.hits  # pylint: disable=pointless-statement
    metatlas_dataset.frag_mz_tolerance = 1e-4
    assert not metatlas_dataset._hits_valid
    assert metatlas_dataset.frag_mz_tolerance == 1e-4


def test_set_msms_refs_loc_setter(metatlas_dataset, mocker, hits):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    metatlas_dataset.hits  # pylint: disable=pointless-statement
    metatlas_dataset.msms_refs_loc = "/tmp/some_file.tab"
    assert not metatlas_dataset._hits_valid
    assert metatlas_dataset.msms_refs_loc == "/tmp/some_file.tab"


def test_set_data01(metatlas_dataset):
    metatlas_dataset.set_data([0, 0, "identification", "ms2_notes"], "extact match")
    assert metatlas_dataset[0][0]["identification"].ms2_notes == "extact match"


def test_store_atlas99(atlas, sqlite, username):
    atlas.name = "test_store_atlas01"
    atlas_list = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(atlas_list) == 0
    metob.store(atlas)
    second = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(second) == 1


def test_store_atlas98(metatlas_dataset, atlas, sqlite, username):
    atlas.name = "test_store_atlas01"
    atlas_list = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(atlas_list) == 0
    metatlas_dataset.store_atlas()
    second = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(second) == 1


def test_store_atlas97(metatlas_dataset, atlas, sqlite, username):
    atlas.name = "test_store_atlas01"
    atlas_list = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(atlas_list) == 0
    metatlas_dataset.store_atlas(name='foobar', even_if_exists=True)
    second = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(second) == 1


def test_store_atlas96(metatlas_dataset, atlas, sqlite, username):
    atlas.name = "test_store_atlas01"
    atlas_list = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(atlas_list) == 0
    metatlas_dataset.store_atlas(name='foobar', even_if_exists=True)
    second = metob.retrieve("Atlas", name=atlas.name, username=username)
    assert len(second) == 1


def test_store_atlas01(metatlas_dataset, sqlite, username):
    metatlas_dataset.atlas.name = "test_store_atlas01"
    atlas_list = metob.retrieve("Atlas", name=metatlas_dataset.atlas.name, username=username)
    assert len(atlas_list) == 0
    metatlas_dataset.store_atlas()
    second = metob.retrieve("Atlas", name=metatlas_dataset.atlas.name, username=username)
    assert len(second) == 1
    metatlas_dataset.store_atlas(even_if_exists=True)
    with pytest.raises(ValueError):
        metatlas_dataset.store_atlas()


def test_analysis_identifiers01(sqlite):
    with pytest.raises(ValueError):
        mads.AnalysisIdentifiers(
            "source_atlas_name_not_valid",
            "experiment_not_valid",
            "output_type_not_valid",
            "polarity_not_valid",
            "analysis_number_not_valid",
            "/foo/bar",
        )


def test_analysis_identifiers02(mocker, sqlite_with_atlas, username):
    with pytest.raises(ValueError):
        mads.AnalysisIdentifiers(
            f"HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_{username}0",
            "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583",
            "output_type_not_valid",
            "polarity_not_valid",
            "analysis_number_not_valid",
            "/foo/bar",
        )


def test_analysis_identifiers03(mocker, username):
    with pytest.raises(ValueError):
        mads.AnalysisIdentifiers(
            f"HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_{username}0",
            "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583",
            "FinalEMA-HILIC",
            "polarity_not_valid",
            "analysis_number_not_valid",
            "/foo/bar",
        )


def test_analysis_identifiers04(mocker, username):
    with pytest.raises(TypeError):
        mads.AnalysisIdentifiers(
            f"HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_{username}0",
            "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583",
            "FinalEMA-HILIC",
            "positive",
            "analysis_number_not_valid",
            "/foo/bar",
        )


def test_analysis_identifiers05(mocker, username):
    with pytest.raises(TypeError):
        mads.AnalysisIdentifiers(
            f"HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_{username}0",
            "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583",
            "FinalEMA-HILIC",
            "positive",
            "1",
            "/foo/bar",
        )


def test_analysis_identifiers06(mocker, username):
    with pytest.raises(ValueError):
        mads.AnalysisIdentifiers(
            f"HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_{username}0",
            "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583",
            "FinalEMA-HILIC",
            "positive",
            -9,
            "/foo/bar",
        )


def test_analysis_identifiers07(mocker, username):
    with pytest.raises(ValueError):
        mads.AnalysisIdentifiers(
            f"HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_{username}0",
            "experiemnt_name_not_valid",
            "output_type_not_valid",
            "polarity_not_valid",
            "analysis_number_not_valid",
            "/foo/bar",
        )


def test_analysis_identifiers_atlas01(analysis_ids, username):
    assert analysis_ids.atlas == f"505892_OakGall_final_POS_{username}0"


def test_analysis_identifiers_atlas02(analysis_ids, username):
    # call .atlas twice to get cached value
    analysis_ids.atlas  # pylint: disable=pointless-statement
    assert analysis_ids.atlas == f"505892_OakGall_final_POS_{username}0"


def test_write_data_source_files01(metatlas_dataset, mocker, caplog):
    mocker.patch("glob.glob", return_value=range(10))
    metatlas_dataset.write_data_source_files()
    assert "Data sources directory already populated" in caplog.text


def test_write_data_source_files02(metatlas_dataset, mocker, caplog):
    mocker.patch("glob.glob", return_value=range(3))
    mocker.patch("shutil.rmtree")
    mocker.patch("metatlas.io.metatlas_get_data_helper_fun.make_data_sources_tables")
    caplog.set_level(logging.INFO)
    metatlas_dataset.write_data_source_files()
    assert "Writing data source files to" in caplog.text
    assert ma_data.make_data_sources_tables.called  # pylint: disable=no-member


def test_get_atlas01(mocker, analysis_ids, df_container, lcmsrun, atlas, username):
    mocker.patch(
        "metatlas.io.metatlas_get_data_helper_fun.df_container_from_metatlas_file", return_value=df_container
    )
    mocker.patch("metatlas.plots.dill2plots.get_metatlas_files", return_value=[lcmsrun])
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[atlas])
    mocker.patch("glob.glob", return_value=range(10))
    metatlas_dataset = mads.MetatlasDataset(analysis_ids)
    assert metatlas_dataset.atlas.name == f"505892_OakGall_final_POS_{username}0"


def test_get_atlas02(mocker, analysis_ids, caplog):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[])
    caplog.set_level(logging.INFO)
    with pytest.raises(ValueError):
        mads.MetatlasDataset(analysis_ids)
    assert "Database does not contain an atlas named" in caplog.text


def test_get_atlas03(mocker, analysis_ids, caplog):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[0, 0])
    with pytest.raises(ValueError):
        mads.MetatlasDataset(analysis_ids)
    assert "Database contains more than one atlas named" in caplog.text


def test_existing_groups(mocker, metatlas_dataset):
    """This test has little value, but is needed for coverage"""
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[])
    assert metatlas_dataset.existing_groups == []


def test_lcmsruns_dataframe(metatlas_dataset):
    assert metatlas_dataset.lcmsruns_dataframe.shape == (1, 15)


def test_store_groups01(metatlas_dataset, mocker):
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[])
    mocker.patch("metatlas.datastructures.metatlas_objects.store")
    metatlas_dataset.store_groups()
    assert metob.store.called  # pylint: disable=no-member


def test_store_groups02(metatlas_dataset, mocker, username):
    def group():
        pass

    group.name = f"20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_POS_MSMS_{username}0_Cone-S1"
    mocker.patch("metatlas.datastructures.metatlas_objects.retrieve", return_value=[group])
    with pytest.raises(ValueError):
        metatlas_dataset.store_groups()


def test_annotation_gui01(metatlas_dataset, hits, mocker):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", return_value=hits)
    agui = metatlas_dataset.annotation_gui()
    agui.compound_idx = 0
    agui.set_msms_flag("1, co-isolated precursor but all reference ions are in sample spectrum")
    agui.set_peak_flag("remove")
    agui.data.set_rt(0, "rt_min", 2.1245)
    agui.data.set_rt(0, "rt_max", 2.4439)
    assert metatlas_dataset.rts[0].rt_min == 2.1245
    assert metatlas_dataset.rts[0].rt_max == 2.4439
    assert metatlas_dataset.data[0][0]["identification"].ms1_notes == "remove"
    assert (
        metatlas_dataset.data[0][0]["identification"].ms2_notes
        == "1, co-isolated precursor but all reference ions are in sample spectrum"
    )


def test_generate_all_outputs01(metatlas_dataset, hits, mocker):
    mocker.patch("metatlas.plots.dill2plots.get_msms_hits", hits)
    metatlas_dataset.generate_all_outputs()
    assert len(glob.glob(metatlas_dataset.ids.output_dir + "/*")) == 12
    assert len(glob.glob(metatlas_dataset.ids.output_dir + "/*/*")) == 23
