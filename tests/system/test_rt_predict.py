# pylint: disable=missing-function-docstring, missing-module-docstring, line-too-long, duplicate-code

from . import utils


def test_targeted_by_line01_with_remove(tmp_path):
    image = "registry.spin.nersc.gov/metatlas_test/metatlas_ci02:v1.3.5"
    experiment = "20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583"
    expected = {}
    expected[
        str(tmp_path / experiment / "root0/data_QC/rt_model.txt")
    ] = """RANSACRegressor(random_state=42)
Linear model with intercept=-0.004 and slope=0.99798
groups = 20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_FPS_MS1_root0_QC, 20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_POS_MSMS_root0_QC
atlas = HILICz150_ANT20190824_TPL_QCv3_Unlab_POS

LinearRegression()
Polynomial model with intercept=0.097 and coefficents=[0.00000, 0.96116, 0.00213]
groups = 20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_FPS_MS1_root0_QC, 20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_POS_MSMS_root0_QC
atlas = HILICz150_ANT20190824_TPL_QCv3_Unlab_POS
"""
    expected[
        str(tmp_path / experiment / "root0/data_QC/RT_Predicted_Model_Comparison.csv")
    ] = """,RT Measured,RT Reference,RT Linear Pred,RT Polynomial Pred,RT Diff Linear,RT Diff Polynomial
0000_4-methoxyphenylacetic_acid_unlabeled_positive_M+H167p0703_1p07,0.7757497429847717,1.068941733,1.062903572946303,1.1269157193507062,-0.28715382996153127,-0.3511659763659345
0001_nicotinamide_unlabeled_positive_M+H123p0553_1p22,1.2491384744644165,1.224396021,1.2180440647072988,1.277093230335882,0.031094409757117747,-0.027954755871465453
0002_thymine_unlabeled_positive_M+H127p0502_1p26,1.6553537845611572,1.255231064,1.248816864840618,1.3068938537656585,0.4065369197205393,0.34845993079549875
0003_benzoic_acid_unlabeled_positive_M+H123p0441_1p27,1.2450578808784485,1.272043637,1.265595500390302,1.323144126044538,-0.020537619511853622,-0.07808624516608953
0004_2_4-dihydroxypteridine_unlabeled_positive_M+H165p0407_1p27,,1.272194658,1.2657462165429905,1.32329010157373,,
0005_uracil_unlabeled_positive_M+H113p0346_1p39,1.8842174410820007,1.393699506,1.3870057978165864,1.4407671152594659,0.49721164326541434,0.44345032582253485
0006_thymidine_unlabeled_positive_M+H243p0975_1p60,1.6583104729652405,1.603927488,1.596809418733121,1.6441748822425457,0.06150105423211949,0.014135590722694769
0007_2-hydroxyphenylacetic_acid_unlabeled_positive_M+H153p0546_1p62,1.3172867894172668,1.616534167,1.6093906501979809,1.656378567437273,-0.29210386078071404,-0.33909177802000623
0008_deoxyuridine_unlabeled_positive_M+H229p0819_1p88,1.9361981749534607,1.876662419,1.8689938136450273,1.9083427073174741,0.06720436130843344,0.027855467635986564
0009_acetylcholine_unlabeled_positive_M146p1176_1p96,1.8230673670768738,1.9552864,1.9474590861922034,1.9845558887665662,-0.12439171911532965,-0.1614885216896924
0010_pyridoxine_unlabeled_positive_M+H170p0812_2p16,2.1844738721847534,2.158057096,2.149820474204603,2.181230854992953,0.03465339798015021,0.0032430171918003126
0011_salicylic_acid_unlabeled_positive_M+H139p0390_2p20,1.8282268047332764,2.196354854,2.1880409252832096,2.2183969913536457,-0.3598141205499332,-0.3901701866203693
0012_2deoxyadenosine_unlabeled_positive_M+H252p1091_2p23,2.293710947036743,2.234006981,2.2256170486168254,2.254942673466113,0.06809389841991775,0.038768273570630285
0013_adenine_unlabeled_positive_M+H136p0618_2p56,2.6646790504455566,2.557601998,2.548558864598047,2.56927787344364,0.11612018584750983,0.09540117700191653
0014_xanthine_unlabeled_positive_M+H153p0407_2p73,2.7709169387817383,2.725344,2.7159622666788823,2.732395658981744,0.054954672102855984,0.03852127979999409
0015_ribose_unlabeled_positive_M+H151p0601_2p75,2.793001413345337,2.750702982,2.741270059655543,2.757066003852173,0.05173135368979409,0.035935409493164094
0016_rhamnose_unlabeled_positive_M+H165p0757_2p80,3.048208475112915,2.796993087,2.787466724577183,2.802106149909774,0.2607417505357321,0.2461023252031409
0017_uridine_unlabeled_positive_M+H245p0768_2p89,2.920204997062683,2.888931519,2.8792195718979,2.8915891009061414,0.040985425164782985,0.028615896156541698
0018_adenosine_unlabeled_positive_M+H268p1040_3p09,3.1090638637542725,3.091018609,3.0808987338207197,3.088405611875559,0.0281651299335528,0.020658251878713507
0019_hypoxanthine_unlabeled_positive_M+H137p0458_3p10,3.1437186002731323,3.102967341,3.092823346401367,3.1000481672384095,0.05089525387176552,0.043670433034722844
0020_5-methylcytosine_unlabeled_positive_M+H126p0662_4p42,4.466769218444824,4.418371688,4.4055724502287985,4.385470549114132,0.06119676821602571,0.08129866933069252
0021_2-oxovaleric_acid_unlabeled_positive_M+H117p0546_4p45,3.9647421836853027,4.448129315,4.435270009207811,4.414635292629683,-0.4705278255225078,-0.44989310894438006
0022_cytosine_unlabeled_positive_M+H112p0505_4p83,4.878586053848267,4.833663875,4.8200263385363336,4.792830070747619,0.05855971531193305,0.0857559831006478
0023_lactic_acid_unlabeled_positive_M+H91p0390_5p06,5.1236891746521,5.064398962,5.050295669310254,5.019475738648949,0.07339350534184597,0.10421343600315058
0024_inosine_unlabeled_positive_M+H269p0880_5p43,5.435921669006348,5.434235961,5.4193861243530295,5.383231720701441,0.01653554465331819,0.052689948304906586
0025_deoxycytidine_unlabeled_positive_M+H228p0979_5p59,5.63983416557312,5.594117397,5.578944827580915,5.540664965694513,0.060889337992205306,0.09916919987860684
0026_nicotinic_acid_unlabeled_positive_M+H124p0393_5p63,5.612481355667114,5.631626786,5.61637850104198,5.577615783318941,-0.0038971453748661844,0.034865572348173224
0027_phenylacetic_acid_unlabeled_positive_M+H137p0597_5p88,6.1643900871276855,5.878913512,5.8631660600806,5.8213702555437035,0.30122402704708584,0.3430198315839821
0028_2_deoxyguanosine_unlabeled_positive_M+H268p1040_6p87,6.9536755084991455,6.87418691,6.856430423443528,6.8050649676035455,0.09724508505561769,0.1486105408956
0029_cytidine_unlabeled_positive_M+H244p0928_6p93,6.825943946838379,6.933566273,6.915689924707814,6.863887108093793,-0.08974597786943495,-0.03794316125541375
0030_N-acetyl-mannosamine_unlabeled_positive_M+Na244p0792_7p15,6.6624157428741455,7.153497474,7.135177177942838,7.081885478010634,-0.4727614350686924,-0.4194697351364889
0031_betaine_unlabeled_positive_M118p0863_7p91,8.0335111618042,7.905109179,7.8852716978638355,7.828449318591656,0.1482394639403637,0.20506184321254306
0032_guanosine_unlabeled_positive_M+H284p0989_8p57,8.48360538482666,8.570944541,8.549763020821363,8.49182598096076,-0.0661576359947027,-0.008220596134099978
0033_phenylalanine_unlabeled_positive_M+H166p0863_8p98,9.09137773513794,8.979305704,8.95729987592511,8.899614864870298,0.13407785921283022,0.19176287026764172
0034_leucine_unlabeled_positive_M+H132p1019_9p32,9.326712608337402,9.319656306,9.296963454490605,9.240032036011817,0.029749153846797327,0.08668057232558546
0035_urocanic_acid_unlabeled_positive_M+H139p0502_9p35,8.878215789794922,9.351932178,9.3291741752016,9.272339873977243,-0.450958385406679,-0.39412408418232125
0036_mannitol_unlabeled_positive_M+H183p0863_9p53,9.116773128509521,9.534507075,9.511380530961908,9.455179262226952,-0.3946074024523867,-0.3384061337174309
0037_isoleucine_unlabeled_positive_M+H132p1019_9p71,9.326712608337402,9.70543744,9.681965860090859,9.626486134780636,-0.35525325175345657,-0.29977352644323396
0038_xanthosine_unlabeled_positive_M+H285p0830_9p78,9.507513999938965,9.782678891,9.759051393379414,9.703938612775616,-0.251537393440449,-0.19642461283665114
0039_tryptophan_unlabeled_positive_M+H205p0972_10p16,10.337260723114014,10.15664925,10.132266864922379,10.079290595303439,0.20499385819163507,0.2579701278105748
0040_methionine_unlabeled_positive_M+H150p0583_10p44,10.456631660461426,10.4409554,10.41599912145348,10.365046300146744,0.04063253900794628,0.09158536031468145
0041_1-methyladenosine_unlabeled_positive_M+H282p1197_10p78,11.042783260345459,10.78124768,10.755604495746342,10.707526942600817,0.2871787645991173,0.3352563177446424
0042_proline_unlabeled_positive_M+H116p0706_10p92,10.849864959716797,10.91977168,10.893848874574285,10.847083243109427,-0.043983914857488315,0.0027817166073695887
0043_pipecolic_acid_unlabeled_positive_M+H130p0863_10p97,10.991784572601318,10.97482181,10.948787881722849,10.902566344225118,0.04299669087846958,0.08921822837620041
0044_valine_unlabeled_positive_M+H118p0863_11p12,11.041275024414062,11.11600911,11.089690184478288,11.044923184166127,-0.048415160064225304,-0.0036481597520641174
0045_5-oxo-proline_unlabeled_positive_M+H130p0499_11p65,11.50427532196045,11.65330736,11.625903857319027,11.58744978041825,-0.1216285353585782,-0.08317445845780114
0046_taurine_unlabeled_positive_M+H126p0219_12p16,12.075395107269287,12.15812344,12.129700927876891,12.098300243547898,-0.05430582060760436,-0.022905136278611238
0047_ectoine_unlabeled_positive_M+H143p0815_12p50,12.36878776550293,12.50349732,12.474377644575776,12.448428911008959,-0.10558987907284667,-0.07964114550602908
0048_carnitine_unlabeled_positive_M+H161p1046_13p29,13.466909408569336,13.28582682,13.25512795330405,13.243410597608959,0.21178145526528525,0.22349881096037727
0049_alanine_unlabeled_positive_M+H90p0550_13p41,13.68701457977295,13.40509074,13.37415113006032,13.364832662828071,0.3128634497126299,0.32218191694487786
0050_sucrose_unlabeled_positive_M+H343p1235_13p45,13.328831672668457,13.44515078,13.414130305839409,13.405631224802201,-0.08529863317095199,-0.07679955213374434
0051_threonine_unlabeled_positive_M+H120p0655_13p49,13.459657192230225,13.48957226,13.458462117721956,13.45087963624058,0.0011950745082689451,0.008777555989643915
0052_cis-4-hydroxy-proline_unlabeled_positive_M+H132p0655_13p67,13.243738651275635,13.67383331,13.642351222854888,13.638660690201752,-0.3986125715792532,-0.39492203892611677
0053_4-guanidinobutanoic_acid_unlabeled_positive_M+H146p0924_13p86,13.88631010055542,13.86132281,13.829462261117298,13.829880536300239,0.056847839438121994,0.056429564255180864
0054_maltose_unlabeled_positive_M+Na365p1054_14p07,13.663294792175293,14.0677773,14.035500007112862,14.040616184637264,-0.3722052149375692,-0.3773213924619707
0055_serine_unlabeled_positive_M+H106p0499_14p31,14.328335285186768,14.31261357,14.279842056582272,14.290765198503442,0.0484932286044959,0.037570086683325954
0056_glutamine_unlabeled_positive_M+H147p0764_14p31,14.320549488067627,14.31275825,14.27998644453475,14.290913093540711,0.04056304353287743,0.02963639452691602
0057_asparagine_unlabeled_positive_M+H133p0608_14p37,14.360477924346924,14.36808894,14.335205445351729,14.347479873380236,0.025272478995194803,0.012998050966688268
0058_gamma-Aminobutyric_acid_unlabeled_positive_M+H104p0706_14p39,14.392436504364014,14.38565257,14.352733621836048,14.365438606423183,0.0397028825279655,0.02699789794083074
0059_alpha-ketoglutaric_acid_unlabeled_positive_M+H147p0288_14p51,,14.50646265,14.473299837551405,14.4890020294111,,
0060_mannosamine_unlabeled_positive_M+H180p0866_14p52,14.69622278213501,14.52081396,14.487622178346628,14.503684552870762,0.20860060378838163,0.19253822926424746
0061_cysteic_acid_unlabeled_positive_M+H170p0118_14p54,14.559170722961426,14.53906337,14.505834750532143,14.522356409474206,0.05333597242928256,0.03681431348721986
0062_N-acetyl-aspartic_acid_unlabeled_positive_M+H176p0553_14p82,14.634858131408691,14.82464623,14.790841139927538,14.81473516440485,-0.15598300851884694,-0.1798770329961581
0063_citrulline_unlabeled_positive_M+H176p1030_15p09,15.141581535339355,15.08943009,15.055090513677682,15.086130811048331,0.08649102166167388,0.055450724291024045
0064_N-alpha-acetyl-lysine_unlabeled_positive_M+H189p1234_15p13,15.190487384796143,15.12986101,15.095439820807439,15.127597632861947,0.09504756398870384,0.0628897519341951
0065_N-acetyl-glutamic_acid_unlabeled_positive_M+H190p0710_15p16,15.118823528289795,15.15757256,15.12309543294764,15.156023222818638,-0.004271904657844772,-0.03719969452884264
0066_raffinose_unlabeled_positive_M+H505p1763_15p53,15.543988227844238,15.53249857,15.497264626436776,15.540931897821977,0.04672360140746257,0.0030563300222610223
0067_glutamic_acid_unlabeled_positive_M+H148p0604_15p94,16.006930351257324,15.93538957,15.899342360478306,15.955218576615934,0.10758799077901848,0.05171177464139021
0068_Aspartic_acid_unlabeled_positive_M+H134p0448_16p13,16.24086856842041,16.13036002,16.093919247877274,16.15595235329566,0.14694932054313625,0.08491621512474978
0069_arginine_unlabeled_positive_M+H175p1190_16p94,16.976414680480957,16.93991539,16.901840469127567,16.991172768800162,0.07457421135339004,-0.014758088319204887
0070_lysine_unlabeled_positive_M+H147p1128_17p01,17.048407554626465,17.01131041,16.973091372879324,17.06496535505383,0.07531618174714083,-0.0165578004273641
0071_ornithine_unlabeled_positive_M+H133p0972_17p04,17.070573806762695,17.03725065,16.998979250542746,17.09178209803637,0.07159455621994937,-0.021208291273673296"""

    expected[
        str(tmp_path / experiment / "root0/data_QC/QC_Measured_RTs.csv")
    ] = """,20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_FPS_MS1_0_QC_Pre_Rg70to1050-CE102040--QC_Run6.h5,20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_POS_MSMS_0_QC_Pre_Rg70to1050-CE102040--QC_Run7.h5,20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_FPS_MS1_0_QC_Post_Rg70to1050-CE102040--QC_Run307.h5,20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583_POS_MSMS_0_QC_Post_Rg70to1050-CE102040--QC_Run308.h5,mean,median,min,max,standard deviation,standard error,#NaNs
0000_4-methoxyphenylacetic_acid_unlabeled_positive_M+H167p0703_1p07,0.760883629322052,0.7883098125457764,0.7816191911697388,0.7698802947998047,0.775173231959343,0.7757497429847717,0.760883629322052,0.7883098125457764,0.012197377682005251,0.006098688841002626,0
0001_nicotinamide_unlabeled_positive_M+H123p0553_1p22,1.2340805530548096,1.2472213506698608,1.2510555982589722,1.2544312477111816,1.246697187423706,1.2491384744644165,1.2340805530548096,1.2544312477111816,0.008911895485740983,0.004455947742870492,0
0002_thymine_unlabeled_positive_M+H127p0502_1p26,1.6460527181625366,1.656285285949707,1.6621986627578735,1.6544222831726074,1.6547397375106812,1.6553537845611572,1.6460527181625366,1.6621986627578735,0.0066730644692519535,0.0033365322346259768,0
0003_benzoic_acid_unlabeled_positive_M+H123p0441_1p27,1.6460527181625366,0.772739052772522,1.7125025987625122,0.8440630435943604,1.2438393533229828,1.2450578808784485,0.772739052772522,1.7125025987625122,0.5043733469961971,0.25218667349809853,0
0004_2_4-dihydroxypteridine_unlabeled_positive_M+H165p0407_1p27,,,,,,,,,,,0
0005_uracil_unlabeled_positive_M+H113p0346_1p39,1.8791532516479492,1.8892816305160522,1.878132700920105,1.8925062417984009,1.8847684562206268,1.8842174410820007,1.878132700920105,1.8925062417984009,0.00720661359839974,0.00360330679919987,0
0006_thymidine_unlabeled_positive_M+H243p0975_1p60,1.6460527181625366,1.6672121286392212,1.6621986627578735,1.6544222831726074,1.6574714481830597,1.6583104729652405,1.6460527181625366,1.6672121286392212,0.009254048049870576,0.004627024024935288,0
0007_2-hydroxyphenylacetic_acid_unlabeled_positive_M+H153p0546_1p62,1.4245437383651733,1.2100298404693604,1.6621986627578735,1.1872817277908325,1.37101349234581,1.3172867894172668,1.1872817277908325,1.6621986627578735,0.22160579729537735,0.11080289864768868,0
0008_deoxyuridine_unlabeled_positive_M+H229p0819_1p88,1.940125823020935,1.9492311477661133,1.910657525062561,1.9322705268859863,1.933071255683899,1.9361981749534607,1.910657525062561,1.9492311477661133,0.016471445184473014,0.008235722592236507,0
0009_acetylcholine_unlabeled_positive_M146p1176_1p96,1.8015246391296387,1.7716032266616821,1.8446100950241089,1.8571667671203613,1.8187261819839478,1.8230673670768738,1.7716032266616821,1.8571667671203613,0.03942977527526356,0.01971488763763178,0
0010_pyridoxine_unlabeled_positive_M+H170p0812_2p16,2.140230655670166,2.1597485542297363,2.2091991901397705,2.2232186794281006,2.1830992698669434,2.1844738721847534,2.140230655670166,2.2232186794281006,0.03947043984935922,0.01973521992467961,0
0011_salicylic_acid_unlabeled_positive_M+H139p0390_2p20,,1.8414007425308228,1.8282268047332764,1.78067147731781,1.816766341527303,1.8282268047332764,1.78067147731781,1.8414007425308228,0.03194554078427394,0.01844376657120873,0
0012_2deoxyadenosine_unlabeled_positive_M+H252p1091_2p23,2.2475903034210205,2.2757790088653564,2.322835922241211,2.31164288520813,2.2894620299339294,2.293710947036743,2.2475903034210205,2.322835922241211,0.03438155307316169,0.017190776536580844,0
0013_adenine_unlabeled_positive_M+H136p0618_2p56,2.593029737472534,2.6252453327178955,2.7041127681732178,2.7198987007141113,2.6605716347694397,2.6646790504455566,2.593029737472534,2.7198987007141113,0.06117021758664283,0.030585108793321415,0
0014_xanthine_unlabeled_positive_M+H153p0407_2p73,2.747974395751953,2.775257110595703,2.7665767669677734,2.788285493850708,2.7695234417915344,2.7709169387817383,2.747974395751953,2.788285493850708,0.01691088242483735,0.008455441212418676,0
0015_ribose_unlabeled_positive_M+H151p0601_2p75,2.763174295425415,2.769817352294922,2.835042953491211,2.816185474395752,2.796055018901825,2.793001413345337,2.763174295425415,2.835042953491211,0.03509440319693131,0.017547201598465654,0
0016_rhamnose_unlabeled_positive_M+H165p0757_2p80,3.136334180831909,2.960082769393921,,,3.048208475112915,3.048208475112915,2.960082769393921,3.136334180831909,0.12462856822150174,0.08812570571899414,0
0017_uridine_unlabeled_positive_M+H245p0768_2p89,2.919912815093994,2.943791389465332,2.917609214782715,2.920497179031372,2.9254526495933533,2.920204997062683,2.917609214782715,2.943791389465332,0.012289227050439883,0.0061446135252199415,0
0018_adenosine_unlabeled_positive_M+H268p1040_3p09,3.075451612472534,3.078127861022949,3.1469616889953613,3.1399998664855957,3.11013525724411,3.1090638637542725,3.075451612472534,3.1469616889953613,0.03862429972687937,0.019312149863439685,0
0019_hypoxanthine_unlabeled_positive_M+H137p0458_3p10,3.136334180831909,3.1404755115509033,3.1469616889953613,3.161953926086426,3.14643132686615,3.1437186002731323,3.136334180831909,3.161953926086426,0.011234715018600752,0.005617357509300376,0
0020_5-methylcytosine_unlabeled_positive_M+H126p0662_4p42,4.396528244018555,4.399042129516602,4.534496307373047,4.545421600341797,4.4688720703125,4.466769218444824,4.396528244018555,4.545421600341797,0.08221155813284872,0.04110577906642436,0
0021_2-oxovaleric_acid_unlabeled_positive_M+H117p0546_4p45,,,,3.9647421836853027,3.9647421836853027,3.9647421836853027,3.9647421836853027,3.9647421836853027,,,0
0022_cytosine_unlabeled_positive_M+H112p0505_4p83,4.836014747619629,4.8464555740356445,4.910716533660889,4.921308994293213,4.878623962402344,4.878586053848267,4.836014747619629,4.921308994293213,0.04359776550856559,0.021798882754282795,0
0023_lactic_acid_unlabeled_positive_M+H91p0390_5p06,,5.1236891746521,,,5.1236891746521,5.1236891746521,5.1236891746521,5.1236891746521,,,0
0024_inosine_unlabeled_positive_M+H269p0880_5p43,5.432004451751709,5.439838886260986,5.39183235168457,5.441697120666504,5.426343202590942,5.435921669006348,5.39183235168457,5.441697120666504,0.023387495592980652,0.011693747796490326,0
0025_deoxycytidine_unlabeled_positive_M+H228p0979_5p59,5.601799011230469,5.607846260070801,5.6718220710754395,5.671968460083008,5.638358950614929,5.63983416557312,5.601799011230469,5.671968460083008,0.03880306263547012,0.01940153131773506,0
0026_nicotinic_acid_unlabeled_positive_M+H124p0393_5p63,5.478054046630859,5.553140640258789,5.6718220710754395,5.700730800628662,5.6009368896484375,5.612481355667114,5.478054046630859,5.700730800628662,0.10387204978316382,0.05193602489158191,0
0027_phenylacetic_acid_unlabeled_positive_M+H137p0597_5p88,,6.089038848876953,6.223822593688965,6.1643900871276855,6.159083843231201,6.1643900871276855,6.089038848876953,6.223822593688965,0.06754836515123151,0.03899906680338265,0
0028_2_deoxyguanosine_unlabeled_positive_M+H268p1040_6p87,6.925775527954102,6.942814826965332,6.964536190032959,6.967518329620361,6.9501612186431885,6.9536755084991455,6.925775527954102,6.967518329620361,0.019634497574413202,0.009817248787206601,0
0029_cytidine_unlabeled_positive_M+H244p0928_6p93,6.8023223876953125,6.832950592041016,6.818937301635742,6.858341693878174,6.828137993812561,6.825943946838379,6.8023223876953125,6.858341693878174,0.023710214782490673,0.011855107391245337,0
0030_N-acetyl-mannosamine_unlabeled_positive_M+Na244p0792_7p15,6.656971454620361,6.657993316650391,6.6668381690979,6.696530342102051,6.669583320617676,6.6624157428741455,6.656971454620361,6.696530342102051,0.018502839238360106,0.009251419619180053,0
0031_betaine_unlabeled_positive_M118p0863_7p91,7.914710998535156,7.898166656494141,8.152311325073242,8.210945129394531,8.044033527374268,8.0335111618042,7.898166656494141,8.210945129394531,0.1608156551761606,0.0804078275880803,0
0032_guanosine_unlabeled_positive_M+H284p0989_8p57,8.49014663696289,8.50051498413086,8.451272010803223,8.47706413269043,8.47974944114685,8.48360538482666,8.451272010803223,8.50051498413086,0.021271924977460343,0.010635962488730171,0
0033_phenylalanine_unlabeled_positive_M+H166p0863_8p98,9.065049171447754,9.064212799072266,9.132002830505371,9.117706298828125,9.094742774963379,9.09137773513794,9.064212799072266,9.132002830505371,0.03525821268363917,0.017629106341819585,0
0034_leucine_unlabeled_positive_M+H132p1019_9p32,9.267672538757324,9.295421600341797,9.358003616333008,9.375864028930664,9.324240446090698,9.326712608337402,9.267672538757324,9.375864028930664,0.051105772604218114,0.025552886302109057,0
0035_urocanic_acid_unlabeled_positive_M+H139p0502_9p35,8.894339561462402,8.865837097167969,8.890594482421875,8.856619834899902,8.876847743988037,8.878215789794922,8.856619834899902,8.894339561462402,0.018487285230656875,0.009243642615328437,0
0036_mannitol_unlabeled_positive_M+H183p0863_9p53,9.065049171447754,9.164083480834961,9.148656845092773,9.08488941192627,9.11566972732544,9.116773128509521,9.065049171447754,9.164083480834961,0.0481037419227615,0.02405187096138075,0
0037_isoleucine_unlabeled_positive_M+H132p1019_9p71,9.267672538757324,9.295421600341797,9.358003616333008,9.375864028930664,9.324240446090698,9.326712608337402,9.267672538757324,9.375864028930664,0.051105772604218114,0.025552886302109057,0
0038_xanthosine_unlabeled_positive_M+H285p0830_9p78,9.526045799255371,9.48938274383545,9.510781288146973,9.504246711730957,9.507614135742188,9.507513999938965,9.48938274383545,9.526045799255371,0.015203949810787694,0.007601974905393847,0
0039_tryptophan_unlabeled_positive_M+H205p0972_10p16,10.33144474029541,10.327781677246094,10.347268104553223,10.343076705932617,10.337392807006836,10.337260723114014,10.327781677246094,10.347268104553223,0.009266094493898432,0.004633047246949216,0
0040_methionine_unlabeled_positive_M+H150p0583_10p44,10.443852424621582,10.439347267150879,10.46941089630127,10.474287986755371,10.456724643707275,10.456631660461426,10.439347267150879,10.474287986755371,0.01767370234818388,0.00883685117409194,0
0041_1-methyladenosine_unlabeled_positive_M+H282p1197_10p78,11.050666809082031,11.034899711608887,,,11.042783260345459,11.042783260345459,11.034899711608887,11.050666809082031,0.011149021542889777,0.007883548736572266,0
0042_proline_unlabeled_positive_M+H116p0706_10p92,10.827990531921387,10.806012153625488,10.871739387512207,10.887017250061035,10.84818983078003,10.849864959716797,10.806012153625488,10.887017250061035,0.03763472791114847,0.018817363955574234,0
0043_pipecolic_acid_unlabeled_positive_M+H130p0863_10p97,10.955867767333984,10.943641662597656,11.027701377868652,11.047686576843262,10.993724346160889,10.991784572601318,10.943641662597656,11.047686576843262,0.05166480677489114,0.02583240338744557,0
0044_valine_unlabeled_positive_M+H118p0863_11p12,11.034863471984863,11.012262344360352,11.061145782470703,11.047686576843262,11.038989543914795,11.041275024414062,11.012262344360352,11.061145782470703,0.020799879441150262,0.010399939720575131,0
0045_5-oxo-proline_unlabeled_positive_M+H130p0499_11p65,11.499093055725098,11.508075714111328,11.50047492980957,11.510473251342773,11.504529237747192,11.50427532196045,11.499093055725098,11.510473251342773,0.00559458905420339,0.002797294527101695,0
0046_taurine_unlabeled_positive_M+H126p0219_12p16,12.104499816894531,12.101568222045898,12.045284271240234,12.049221992492676,12.075143575668335,12.075395107269287,12.045284271240234,12.104499816894531,0.03226741065106046,0.01613370532553023,0
0047_ectoine_unlabeled_positive_M+H143p0815_12p50,12.293835639953613,12.278909683227539,12.455086708068848,12.443739891052246,12.367892980575562,12.36878776550293,12.278909683227539,12.455086708068848,0.09444225193198486,0.04722112596599243,0
0048_carnitine_unlabeled_positive_M+H161p1046_13p29,,13.355096817016602,,13.57872200012207,13.466909408569336,13.466909408569336,13.355096817016602,13.57872200012207,0.15812688341796033,0.11181259155273438,0
0049_alanine_unlabeled_positive_M+H90p0550_13p41,,13.68701457977295,,,13.68701457977295,13.68701457977295,13.68701457977295,13.68701457977295,,,0
0050_sucrose_unlabeled_positive_M+H343p1235_13p45,,,13.34303092956543,13.314632415771484,13.328831672668457,13.328831672668457,13.314632415771484,13.34303092956543,0.02008078167931844,0.014199256896972656,0
0051_threonine_unlabeled_positive_M+H120p0655_13p49,13.462236404418945,13.455792427062988,13.457077980041504,13.46524429321289,13.460087776184082,13.459657192230225,13.455792427062988,13.46524429321289,0.004423993974227501,0.0022119969871137505,0
0052_cis-4-hydroxy-proline_unlabeled_positive_M+H132p0655_13p67,13.227526664733887,13.222009658813477,13.259950637817383,13.277363777160645,13.246712684631348,13.243738651275635,13.222009658813477,13.277363777160645,0.026413858243097502,0.013206929121548751,0
0053_4-guanidinobutanoic_acid_unlabeled_positive_M+H146p0924_13p86,13.855559349060059,13.86020565032959,13.917991638183594,13.91241455078125,13.886542797088623,13.88631010055542,13.855559349060059,13.917991638183594,0.03322647837942044,0.01661323918971022,0
0054_maltose_unlabeled_positive_M+Na365p1054_14p07,13.650632858276367,13.675956726074219,13.638050079345703,13.978111267089844,13.735687732696533,13.663294792175293,13.638050079345703,13.978111267089844,0.16238268195258865,0.08119134097629432,0
0055_serine_unlabeled_positive_M+H106p0499_14p31,14.32981014251709,14.33325481414795,14.326860427856445,14.324366569519043,14.328572988510132,14.328335285186768,14.324366569519043,14.33325481414795,0.0038330521372662756,0.0019165260686331378,0
0056_glutamine_unlabeled_positive_M+H147p0764_14p31,14.314238548278809,14.306297302246094,14.326860427856445,14.336118698120117,14.320878744125366,14.320549488067627,14.306297302246094,14.336118698120117,0.013225573537406289,0.006612786768703144,0
0057_asparagine_unlabeled_positive_M+H133p0608_14p37,14.36136245727539,14.355669021606445,14.359593391418457,14.37166690826416,14.362072944641113,14.360477924346924,14.355669021606445,14.37166690826416,0.006824156717503251,0.0034120783587516254,0
0058_gamma-Aminobutyric_acid_unlabeled_positive_M+H104p0706_14p39,14.37686824798584,14.366856575012207,14.408004760742188,14.413251876831055,14.391245365142822,14.392436504364014,14.366856575012207,14.413251876831055,0.022852268153811535,0.011426134076905767,0
0059_alpha-ketoglutaric_acid_unlabeled_positive_M+H147p0288_14p51,,,,,,,,,,,0
0060_mannosamine_unlabeled_positive_M+H180p0866_14p52,14.704928398132324,14.712645530700684,14.6831636428833,14.687517166137695,14.697063684463501,14.69622278213501,14.6831636428833,14.712645530700684,0.014011838106020863,0.007005919053010431,0
0061_cysteic_acid_unlabeled_positive_M+H170p0118_14p54,14.579874992370605,14.584083557128906,14.537906646728516,14.538466453552246,14.560082912445068,14.559170722961426,14.537906646728516,14.584083557128906,0.025343082088378755,0.012671541044189378,0
0062_N-acetyl-aspartic_acid_unlabeled_positive_M+H176p0553_14p82,,14.561990737915039,14.634858131408691,14.699416160583496,14.632088343302408,14.634858131408691,14.561990737915039,14.699416160583496,0.06875456707387731,0.03969546780811925,0
0063_citrulline_unlabeled_positive_M+H176p1030_15p09,15.128581047058105,15.128291130065918,15.154582023620605,15.162788391113281,15.143560647964478,15.141581535339355,15.128291130065918,15.162788391113281,0.017783170397114904,0.008891585198557452,0
0064_N-alpha-acetyl-lysine_unlabeled_positive_M+H189p1234_15p13,15.159500122070312,15.161605834960938,15.219368934631348,15.223294258117676,15.190942287445068,15.190487384796143,15.159500122070312,15.223294258117676,0.03513764118653772,0.01756882059326886,0
0065_N-acetyl-glutamic_acid_unlabeled_positive_M+H190p0710_15p16,15.144072532653809,15.128291130065918,15.105835914611816,15.109355926513672,15.121888875961304,15.118823528289795,15.105835914611816,15.144072532653809,0.017775225003882934,0.008887612501941467,0
0066_raffinose_unlabeled_positive_M+H505p1763_15p53,15.555009841918945,15.555731773376465,15.516404151916504,15.532966613769531,15.540028095245361,15.543988227844238,15.516404151916504,15.555731773376465,0.018964998104185705,0.009482499052092853,0
0067_glutamic_acid_unlabeled_positive_M+H148p0604_15p94,16.00358009338379,16.012876510620117,16.00017547607422,16.01028060913086,16.006728172302246,16.006930351257324,16.00017547607422,16.012876510620117,0.005867142979506786,0.002933571489753393,0
0068_Aspartic_acid_unlabeled_positive_M+H134p0448_16p13,16.245359420776367,16.244237899780273,16.233556747436523,16.237499237060547,16.240163326263428,16.24086856842041,16.233556747436523,16.245359420776367,0.00560790521224537,0.002803952606122685,0
0069_arginine_unlabeled_positive_M+H175p1190_16p94,16.963918685913086,16.961685180664062,16.988910675048828,16.9918212890625,16.97658395767212,16.976414680480957,16.961685180664062,16.9918212890625,0.01598443924833885,0.007992219624169425,0
0070_lysine_unlabeled_positive_M+H147p1128_17p01,17.043212890625,17.035064697265625,17.05360221862793,17.05995750427246,17.047959327697754,17.048407554626465,17.035064697265625,17.05995750427246,0.011024194876641502,0.005512097438320751,0
0071_ornithine_unlabeled_positive_M+H133p0972_17p04,17.058874130249023,17.06319236755371,17.085508346557617,17.07795524597168,17.071382522583008,17.070573806762695,17.058874130249023,17.085508346557617,0.0124669979531353,0.00623349897656765,0"""
    command = """\
                    jq -M '(.cells[] | select(.source[] | contains("predict_rt.generate_rt_correction_models(ids, max_cpus, metatlas_repo_path)")).source) \
                                = ["predict_rt.generate_rt_correction_models(ids, max_cpus, metatlas_repo_path, model_only=True)"]' \
                                /src/notebooks/reference/RT_Prediction.ipynb > /out/Remove.ipynb &&  \
                    papermill \
                        -p source_atlas HILICz150_ANT20190824_PRD_EMA_Unlab_POS_20201106_505892_root0 \
                        -p experiment 20201106_JGI-AK_PS-KM_505892_OakGall_final_QE-HF_HILICZ_USHXG01583 \
                        -p metatlas_repo_path /src \
                        -p project_directory /out \
                        -p max_cpus 2 \
                        /out/Remove.ipynb \
                        /out/Remove-done.ipynb
                   """
    utils.exec_docker(image, command, tmp_path)
    assert utils.num_files_in(tmp_path) == 8
    utils.assert_files_match(expected)
