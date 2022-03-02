-- Use this file to generate a near-minimal database for testing
-- to generate an sqlite3 database run:
-- mysql_to_sqlite_filtered.sh c18_test_case_from_db.sql <mysql_password>

-- remove tables that are not used
DROP TABLE IF EXISTS Compounds;
DROP TABLE IF EXISTS `Group`;
DROP TABLE IF EXISTS `group`;

-- clean out tables we don't need pre-populated values in
DELETE FROM groups;
DELETE FROM groups_items;
DELETE FROM methods;
DELETE FROM samples;
DELETE FROM mzintensitypairs;
DELETE FROM identificationgrades;
DELETE FROM functionalsets;
DELETE FROM fragmentationreferences_mz_intensities;
DELETE FROM compoundidentifications_frag_references;
DELETE FROM fragmentationreferences;

-- keep atlas with name 'C18_20220118_TPL_NEG'
DELETE FROM atlases
WHERE unique_id!='f74a731c590544aba5c3720b346e508e';

UPDATE atlases
SET username='root'
WHERE unique_id='f74a731c590544aba5c3720b346e508e';

DELETE l
FROM lcmsruns AS l
LEFT JOIN (
	SELECT unique_id
	FROM lcmsruns AS l1
	JOIN (
		SELECT MAX(creation_time) AS ctime, hdf5_file
		FROM lcmsruns
		WHERE name LIKE '20210915\_JGI-AK\_MK\_506588\_SoilWaterRep\_final\_QE-HF\_C18\_USDAY63680\_NEG\_MSMS%Run2__.mzML'
		GROUP BY hdf5_file
	) AS early
	ON l1.creation_time=early.ctime AND l1.hdf5_file=early.hdf5_file
) AS j
ON l.unique_id=j.unique_id
WHERE j.unique_id is NULL;

DELETE FROM compounds
WHERE inchi_key NOT IN (
   'FBBCSYADXYILEH-UHFFFAOYSA-N',
   'BDJRBEYXGGNYIS-UHFFFAOYSA-N',
   'OMZRMXULWNMRAE-BMRADRMJSA-N'
);

-- work from compounds up to atlases_compound_identifications
DELETE cic
FROM compoundidentifications_compound AS cic
LEFT JOIN compounds AS c
ON cic.target_id=c.unique_id
WHERE c.unique_id is null;

DELETE ci
FROM compoundidentifications AS ci
LEFT JOIN compoundidentifications_compound AS cic
ON ci.unique_id=cic.source_id
WHERE cic.source_id is null;

DELETE aci
FROM atlases_compound_identifications AS aci
LEFT JOIN compoundidentifications AS ci
ON aci.target_id=ci.unique_id
WHERE ci.unique_id is null;

-- work from atlases_compound_identifications down to everything else
DELETE atlases_compound_identifications
FROM atlases_compound_identifications
LEFT JOIN atlases
ON atlases.unique_id=atlases_compound_identifications.source_id
WHERE atlases.unique_id is null;

DELETE compoundidentifications
FROM compoundidentifications
LEFT JOIN atlases_compound_identifications AS aci
ON aci.target_id=compoundidentifications.unique_id
WHERE aci.target_id is null;

DELETE compoundidentifications_compound
FROM compoundidentifications_compound
LEFT JOIN compoundidentifications AS ci
ON ci.unique_id=compoundidentifications_compound.head_id
WHERE ci.unique_id is null;

DELETE compoundidentifications_rt_references
FROM compoundidentifications_rt_references
LEFT JOIN compoundidentifications AS ci
ON ci.unique_id=compoundidentifications_rt_references.head_id
WHERE ci.unique_id is null;

DELETE compoundidentifications_mz_references
FROM compoundidentifications_mz_references
LEFT JOIN compoundidentifications AS ci
ON ci.unique_id=compoundidentifications_mz_references.head_id
WHERE ci.unique_id is null;

DELETE compounds
FROM compounds
LEFT JOIN compoundidentifications_compound AS cic
ON compounds.head_id=cic.target_id
WHERE cic.target_id is null;

DELETE rtreferences
FROM rtreferences
LEFT JOIN compoundidentifications_rt_references AS cirr
ON rtreferences.head_id=cirr.target_id
WHERE cirr.target_id is null;

DELETE mzreferences
FROM mzreferences
LEFT JOIN compoundidentifications_mz_references AS cimr
ON mzreferences.head_id=cimr.target_id
WHERE cimr.target_id is null;
