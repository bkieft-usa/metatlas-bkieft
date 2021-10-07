# pylint: disable=missing-function-docstring, missing-module-docstring, line-too-long, duplicate-code

from . import utils


def test_add_msms_ref_by_line01(tmp_path):
    image = "registry.spin.nersc.gov/metatlas_test/metatlas_ci01:v1.4.4"
    expected = {}
    expected[
        str(tmp_path / "post_sed.tab")
    ] = """database	id	name	spectrum	decimal	precursor_mz	polarity	adduct	fragmentation_method	collision_energy	instrument	instrument_type	formula	exact_mass	inchi_key	inchi\tsmiles
metatlas	8257da2871be46cfabe10827aaf8d288	L-threonic acid	[[55.7172, 56.1914, 58.0045, 59.0093, 59.0124, 71.0124, 72.9917, 73.0329, 75.0073, 76.0107, 87.0073, 87.212, 89.023, 90.2418, 117.018, 135.029, 135.125, 135.148, 136.032], [6911.62, 9049.5, 11019.7, 7863.62, 293886.0, 204550.0, 763526.0, 7819.21, 4151310.0, 42595.5, 47822.2, 8750.14, 448975.0, 8417.63, 118314.0, 1445940.0, 8032.76, 9857.3, 38018.3]]	4	135.03	negative						C4H8O5	136.037173356	JPIJQSOTBSSVTP-STHAYSLISA-N	InChI=1S/C4H8O5/c5-1-2(6)3(7)4(8)9/h2-3,5-7H,1H2,(H,8,9)/t2-,3+/m0/s1\t
NorthernLabAddition:NoDB	REPLACED_UUID	adenosine	[[55.01269, 57.02821, 66.78931, 69.02660, 71.00568, 73.02122, 78.05609, 80.87838, 85.02310, 87.03920, 89.87952, 89.94361, 104.36960, 107.86694, 115.03886, 119.03568, 133.04977, 136.06194, 170.63907, 268.10406], [186032.312, 313596.656, 99986.633, 100581.734, 145571.344, 267841.375, 126804.180, 109123.148, 375497.844, 116243.438, 103804.906, 103371.594, 139217.422, 110503.422, 296771.406, 123998.859, 488822.156, 54508756.000, 102044.547, 18234916.000]]\t4	268.1037292480469	positive	[M+H]+	CID	23.3eV	ThermoQTOF-3000	Orbitrap	C10H13N5O4	267.096753896	OIRDTQYFTABQOQ-KQYNXXCUSA-N	InChI=1S/C10H13N5O4/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(18)6(17)4(1-16)19-10/h2-4,6-7,10,16-18H,1H2,(H2,11,12,13)/t4-,6-,7-,10-/m1/s1	Nc1ncnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O"""
    command = """head -2 /global/project/projectdirs/metatlas/projects/spectral_libraries/msms_refs_v3.tab > /out/short_refs.tab && \
                    jq -M '(.cells[] | select(.source[] | contains("display_inputs_ui")).source) \
                                += ["\n",
                                    "import ipysheet\n",
                                    "sheet = ipysheet.current()\n",
                                    "input_list = [\\"adenosine\\",\\"InChI=1S/C10H13N5O4/c11-8-5-9(13-2-12-8)15(3-14-5)10-7(18)6(17)4(1-16)19-10/h2-4,6-7,10,16-18H,1H2,(H2,11,12,13)/t4-,6-,7-,10-/m1/s1\\",\\"[M+H]+\\",\\"ThermoQTOF-3000\\", \\"Orbitrap\\", \\"CID\\", \\"12\\", \\"2.9\\", \\"3.3\\", \\"/project/projectdirs/metatlas/raw_data/akuftin/20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583/20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_POS_MSMS_57_Cone-S2_1_Rg70to1050-CE102040-QlobataAkingi-S1_Run40.h5\\"]\n",
                                    "sheet.cells[0].value[0] = input_list\n",
                                    "amr.generate_msms_refs(input_file_name, output_file_name, sheet, validate_input_file)"]' \
                                /src/notebooks/reference/Add_MSMS_Reference.ipynb > /out/Remove.ipynb &&  \
                    papermill \
                        -p metatlas_repo_path /src \
                        -p input_file_name /out/short_refs.tab \
                        -p output_file_name /out/updated_refs.tab \
                        -p num_rows_to_add 1 \
                        /out/Remove.ipynb \
                        /out/Remove-done.ipynb && \
                        sed 's%^NorthernLabAddition:NoDB\t[a-z0-9-]*%NorthernLabAddition:NoDB\tREPLACED_UUID%' < /out/updated_refs.tab > /out/post_sed.tab
                   """
    utils.exec_docker(image, command, tmp_path)
    assert utils.num_files_in(tmp_path) == 5
    utils.assert_files_match(expected)