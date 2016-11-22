#!/usr/bin/perl

use DBI;
use DBD::mysql;
use CGI;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use Net::SMTP;
# libconfig-inifiles-perl
use Config::IniFiles;
# libtext-csv-perl
use Text::CSV;

# Read in configuration
$config = Config::IniFiles->new( -file => "/etc/apache2/bigdatasummerinst.ini" );
$platform = $config->val('database', 'platform');
$database = $config->val('database', 'database');
$host = $config->val('database', 'host');
$port = $config->val('database', 'port');
$tablename = $config->val('database', 'tablename');
$user = $config->val('database', 'user');
$pw = $config->val('database', 'pass');

# Construct DSN
$dsn = "DBI:$platform:$database:$host:$port";

# Connect to database

# PERL DBI CONNECT
$dbh = DBI->connect($dsn, $user, $pw);

# Maximum upload file size of 50 MB
$CGI::POST_MAX = 1024 * $config->val('global', 'postmax');
$uploadDir = $config->val('global', 'uploaddir');

# Initialize variables
$orderNumber = "";
$registrationTime = "";

$firstName = "";
$lastName = "";
$dateOfBirth = "";
$eMailAddress = "";
$phoneNumber = "";

$streetAddress = "";
$cityOfResidence = "";
$stateProvinceRegion = "";
$zipOrPostcode = "";
$countryOfResidence = "";

$isPermanentAddress = "9";

$p_streetAddress = "";
$p_cityOfResidence = "";
$p_stateProvinceRegion = "";
$p_zipOrPostcode = "";
$p_countryOfResidence = "";

$isUSCitizenOrPR = "9";

$reportedEthnicity = "";
$reportedGender = "9";
$currentUniversity = "";
$academicLevel = "";
$expectedGradDate = "";
$overallCollegeGPA = "";
$overallHighSchoolGPA = "";
$standardizedTestType = "";
$standardizedTestScore = "";

$participateToLearn = "";
$participateForResume = "";
$participateForMoney = "";
$participateForNetworking = "";
$participateForOther = "";
$participateForOtherText = "";

$goalGradSchool = "";
$goalWorkIndustry = "";
$goalWorkLab = "";
$goalWorkOther = "";
$goalWorkOtherText = "";

$whatIsDreamJob = "";

$familiarityC = "9";
$familiarityJava = "9";
$familiarityPython = "9";
$familiarityMATLAB = "9";
$familiarityR = "9";

$coursesTaken = "";
$awardsOrHonors = "";

$rankGenomics = "9";
$rankEHR = "9";
$rankMachineLearning = "9";
$rankDataMining = "9";

$referenceOneFirstName = "";
$referenceOneLastName = "";
$referenceOneTitle = "";
$referenceOneRelationship = "";
$referenceOneInstitution = "";
$referenceOneStreetAddress = "";
$referenceOneCityOfResidence = "";
$referenceOneStateProvinceRegion = "";
$referenceOneZipOrPostcode = "";
$referenceOneCountryOfResidence = "";
$referenceOnePhoneNumber = "";
$referenceOneEMailAddress = "";

$isSubmittingSecondReference = "";

$referenceTwoFirstName = "";
$referenceTwoLastName = "";
$referenceTwoTitle = "";
$referenceTwoRelationship = "";
$referenceTwoInstitution = "";
$referenceTwoStreetAddress = "";
$referenceTwoCityOfResidence = "";
$referenceTwoStateProvinceRegion = "";
$referenceTwoZipOrPostcode = "";
$referenceTwoCountryOfResidence = "";
$referenceTwoPhoneNumber = "";
$referenceTwoEMailAddress = "";

$uploadPersonalStatement = "1";
$personalStatementFile = "";
$cvOrResumeFile = "";
$cvOrResume = "";
$personalStatement = "";
$mailLetterOfRec = "9";
$mailUnofficialTrans = "9";
$unofficialTransFile = "";

$foundOutProfAtOwnUni = "";
$foundOutWebSearch = "";
$foundOutPastParticipant = "";
$foundOutAdvertisment = "";
$foundOutOther = "";
$foundOutOtherText = "";

# Grab and parse the input
$query = new CGI;

$firstName = $query->param("firstName");
$lastName = $query->param("lastName");
$dateOfBirth = $query->param("dateOfBirth");
$eMailAddress = $query->param("eMailAddress");
$phoneNumber = $query->param("phoneNumber");
$streetAddress = $query->param("streetAddress");
$cityOfResidence = $query->param("cityOfResidence");
$stateProvinceRegion = $query->param("stateProvinceRegion");
$zipOrPostcode = $query->param("zipOrPostcode");
$countryOfResidence = $query->param("countryOfResidence");
$isPermanentAddress = $query->param("isPermanentAddress");
$p_streetAddress = $query->param("p_streetAddress");
$p_cityOfResidence = $query->param("p_cityOfResidence");
$p_stateProvinceRegion = $query->param("p_stateProvinceRegion");
$p_zipOrPostcode = $query->param("p_zipOrPostcode");
$p_countryOfResidence = $query->param("p_countryOfResidence");
$isUSCitizenOrPR = $query->param("isUSCitizenOrPR");
$reportedEthnicity = $query->param("reportedEthnicity");
$reportedGender = $query->param("reportedGender");
$currentUniversity = $query->param("currentUniversity");
$academicLevel = $query->param("academicLevel");
$expectedGradDate = $query->param("expectedGradDate");
$overallCollegeGPA = $query->param("overallCollegeGPA");
$overallHighSchoolGPA = $query->param("overallHighSchoolGPA");
$standardizedTestType = $query->param("standardizedTestType");
$standardizedTestScore = $query->param("standardizedTestScore");
$participateToLearn = $query->param("participateToLearn");
$participateForResume = $query->param("participateForResume");
$participateForMoney = $query->param("participateForMoney");
$participateForNetworking = $query->param("participateForNetworking");
$participateForOther = $query->param("participateForOther");
$participateForOtherText = $query->param("participateForOtherText");
$goalGradSchool = $query->param("goalGradSchool");
$goalWorkIndustry = $query->param("goalWorkIndustry");
$goalWorkLab = $query->param("goalWorkLab");
$goalWorkOther = $query->param("goalWorkOther");
$goalWorkOtherText = $query->param("goalWorkOtherText");
$whatIsDreamJob = $query->param("whatIsDreamJob");
$familiarityC = $query->param("familiarityC");
$familiarityJava = $query->param("familiarityJava");
$familiarityPython = $query->param("familiarityPython");
$familiarityMATLAB = $query->param("familiarityMATLAB");
$familiarityR = $query->param("familiarityR");
$coursesTaken = $query->param("coursesTaken");
$awardsOrHonors = $query->param("awardsOrHonors");
$rankGenomics = $query->param("rankGenomics");
$rankEHR = $query->param("rankEHR");
$rankMachineLearning = $query->param("rankMachineLearning");
$rankDataMining = $query->param("rankDataMining");
$referenceOneFirstName = $query->param("referenceOneFirstName");
$referenceOneLastName = $query->param("referenceOneLastName");
$referenceOneTitle = $query->param("referenceOneTitle");
$referenceOneRelationship = $query->param("referenceOneRelationship");
$referenceOneInstitution = $query->param("referenceOneInstitution");
$referenceOneStreetAddress = $query->param("referenceOneStreetAddress");
$referenceOneCityOfResidence = $query->param("referenceOneCityOfResidence");
$referenceOneStateProvinceRegion = $query->param("referenceOneStateProvinceRegion");
$referenceOneZipOrPostcode = $query->param("referenceOneZipOrPostcode");
$referenceOneCountryOfResidence = $query->param("referenceOneCountryOfResidence");
$referenceOnePhoneNumber = $query->param("referenceOnePhoneNumber");
$referenceOneEMailAddress = $query->param("referenceOneEMailAddress");
$isSubmittingSecondReference = $query->param("isSubmittingSecondReference");
$referenceTwoFirstName = $query->param("referenceTwoFirstName");
$referenceTwoLastName = $query->param("referenceTwoLastName");
$referenceTwoTitle = $query->param("referenceTwoTitle");
$referenceTwoRelationship = $query->param("referenceTwoRelationship");
$referenceTwoInstitution = $query->param("referenceTwoInstitution");
$referenceTwoStreetAddress = $query->param("referenceTwoStreetAddress");
$referenceTwoCityOfResidence = $query->param("referenceTwoCityOfResidence");
$referenceTwoStateProvinceRegion = $query->param("referenceTwoStateProvinceRegion");
$referenceTwoZipOrPostcode = $query->param("referenceTwoZipOrPostcode");
$referenceTwoCountryOfResidence = $query->param("referenceTwoCountryOfResidence");
$referenceTwoPhoneNumber = $query->param("referenceTwoPhoneNumber");
$referenceTwoEMailAddress = $query->param("referenceTwoEMailAddress");
$uploadPersonalStatement = $query->param("uploadPersonalStatement");
$personalStatementFile = $query->param("personalStatementFile");
$cvOrResumeFile = $query->param("cvOrResumeFile");
$personalStatement = $query->param("personalStatement");
$cvOrResume = $query->param("cvOrResume");
$mailLetterOfRec = $query->param("mailLetterOfRec");
$mailUnofficialTrans = $query->param("mailUnofficialTrans");
$unofficialTransFile = $query->param("unofficialTransFile");
$foundOutProfAtOwnUni = $query->param("foundOutProfAtOwnUni");
$foundOutWebSearch = $query->param("foundOutWebSearch");
$foundOutPastParticipant = $query->param("foundOutPastParticipant");
$foundOutAdvertisment = $query->param("foundOutAdvertisment");
$foundOutOther = $query->param("foundOutOther");
$foundOutOtherText = $query->param("foundOutOtherText");

# Fix up a few sentinel values that CGI:: would have overwritten with nulls.
if ($isPermanentAddress eq "") {
    $isPermanentAddress = 9;
}

if ($isUSCitizenOrPR eq "") {
    $isUSCitizenOrPR = 9;
}

if ($reportedGender eq "") {
    $reportedGender = 9;
}

if ($familiarityC eq "") {
    $familiarityC = 9;
}

if ($familiarityJava eq "") {
    $familiarityJava = 9;
}

if ($familiarityPython eq "") {
    $familiarityPython = 9;
}

if ($familiarityMATLAB eq "") {
    $familiarityMATLAB = 9;
}

if ($familiarityR eq "") {
    $familiarityR = 9;
}

if ($rankGenomics eq "") {
    $rankGenomics = 9;
}

if ($rankEHR eq "") {
    $rankEHR = 9;
}

if ($rankMachineLearning eq "") {
    $rankMachineLearning = 9;
}

if ($rankDataMining eq "") {
    $rankDataMining = 9;
}

if ($uploadPersonalStatement eq "") {
    $uploadPersonalStatement = 1;
}

if ($mailLetterOfRec eq "") {
    $mailLetterOfRec = 9;
}

if ($mailUnofficialTrans eq "") {
    $mailUnofficialTrans = 9;
}

# Log intermediate output (we can get rid of this when done with test and debug)
open LOGFILE, ">/tmp/intermediate.log";
print LOGFILE "FN: " . $firstName . " LN: " . $lastName . " DOB: " . $dateOfBirth . "\n";
print LOGFILE "Email: " . $eMailAddress . " Ph: " . $phoneNumber . "\n";
print LOGFILE "Street: " . $streetAddress . " City:  " . $cityOfResidence . " State: " . $stateProvinceRegion . " ZIP: " . $zipOrPostcode . "\n";
print LOGFILE "Country: " . $countryOfResidence . "\n";
print LOGFILE "Ethni: ". $reportedEthnicity . "\n";
print LOGFILE "Gend: " . $reportedGender . "\n";
print LOGFILE "Is Perm Addr? " . $isPermanentAddress . " Is US Citizen? " . $isUSCitizenOrPR . "\n";
print LOGFILE "PStreet: " . $p_streetAddress . " PCity: " . $p_cityOfResidence . " PState: " . $p_stateProvinceRegion . " PZIP: " . $p_zipOrPostcode . "\n";
print LOGFILE "PCountry: " . $p_countryOfResidence . "\n";
print LOGFILE "Uni: " . $currentUniversity . " Lev: " . $academicLevel . " EGD: " . $expectedGradDate . " colGPA: " . $overallCollegeGPA . " hsGPA: " . $overallHighSchoolGPA . " Test: " . $standardizedTestType . " Score: " . $standardizedTestScore . "\n";
print LOGFILE "Participate to learn: [" . $participateToLearn . "] Resume: [" . $participateForResume . "] Money: [" . $participateForMoney . "] Network: [" . $participateForNetworking . "] Other: [" . $participateForOther . "] Other txt: " . $participateForOtherText . "\n";
print LOGFILE "Goal GS: [" . $goalGradSchool . "] JInd: [" . $goalWorkIndustry . "] JLab: [" . $goalWorkLab . "] Other: [" . $goalWorkOther . "] Other txt: " . $goalWorkOtherText . "\n";
print LOGFILE "DJ: " . $whatIsDreamJob . "\n";
print LOGFILE "FamC: " . $familiarityC . " FamJav: " . $familiarityJava . " FamPy: " . $familiarityPython . " FamMAT: " . $familiarityMATLAB . " FamR: " . $familiarityR . "\n";
print LOGFILE "Courses: " . $coursesTaken . " Awards: " . $awardsOrHonors . "\n";
print LOGFILE "Rank Geno: " . $rankGenomics . " EHR: " . $rankEHR . " ML: " . $rankMachineLearning . " Data mining: " . $rankDataMining . "\n";
print LOGFILE "Ref 1 FN: " . $referenceOneFirstName . " LN: " . $referenceOneLastName . " Rel:  " . $referenceOneRelationship . "\n";
print LOGFILE "Ref 1 Ttl: " . $referenceOneTitle . " Inst: " . $referenceOneInstitution . "\n";
print LOGFILE "Ref 1 Street: " . $referenceOneStreetAddress . " City: " . $referenceOneCityOfResidence . " State: " . $referenceOneStateProvinceRegion . "\n";
print LOGFILE "Ref 1 ZIP: " . $referenceOneZipOrPostcode . " Country: " . $referenceOneCountryOfResidence . "\n";
print LOGFILE "Ref 1 Ph: " . $referenceOnePhoneNumber . " Email: " . $referenceOneEMailAddress . "\n";
print LOGFILE "Submit 2 refs? [" . $isSubmittingSecondReference . "]\n";
print LOGFILE "Ref 2 FN: " . $referenceTwoFirstName . " LN: " . $referenceTwoLastName . " Rel: " . $referenceTwoRelationship . "\n";
print LOGFILE "Ref 2 Ttl: " . $referenceTwoTitle . " Inst: " . $referenceTwoInstitution . "\n";
print LOGFILE "Ref 2 Street: " . $referenceTwoStreetAddress . " City: " . $referenceTwoCityOfResidence . " State: " . $referenceTwoStateProvinceRegion . "\n";
print LOGFILE "Ref 2 ZIP: " . $referenceTwoZipOrPostcode . " Country: " . $referenceTwoCountryOfResidence . "\n";
print LOGFILE "Ref 2 Ph: " . $referenceTwoPhoneNumber . " Email: " . $referenceTwoEMailAddress . "\n";
print LOGFILE "Upload personal: " . $uploadPersonalStatement . " Mail LoR: " . $mailLetterOfRec . " Mail trns: " . $mailUnofficialTrans . "\n";
print LOGFILE "Pers stat file: " . $personalStatementFile . "\n";
print LOGFILE "Unof trans file: " . $unofficialTransFile . "\n";
print LOGFILE "CV or res file: " . $cvOrResumtFile . "\n";
print LOGFILE "Found out Prof: [" . $foundOutProfAtOwnUni . "] Ad: [" . $foundOutAdvertisment . "] Web: [" . $foundOutWebSearch . "] PastPart: [" . $foundOutPastParticipant . "] Other: [" . $foundOutOther . "] Other txt: " . $foundOutOtherText . "\n";
print LOGFILE "\n\n";

# Sanitize input
$firstName = sanitize($firstName);
$lastName = sanitize($lastName);
$dateOfBirth = sanitize($dateOfBirth);
$eMailAddress = sanitize($eMailAddress);
$phoneNumber = sanitize($phoneNumber);
$streetAddress = sanitize($streetAddress);
$cityOfResidence = sanitize($cityOfResidence);
$stateProvinceRegion = sanitize($stateProvinceRegion);
$zipOrPostcode = sanitize($zipOrPostcode);
$countryOfResidence = sanitize($countryOfResidence);
$isPermanentAddress = sanitize($isPermanentAddress);
$p_streetAddress = sanitize($p_streetAddress);
$p_cityOfResidence = sanitize($p_cityOfResidence);
$p_stateProvinceRegion = sanitize($p_stateProvinceRegion);
$p_zipOrPostcode = sanitize($p_zipOrPostcode);
$p_countryOfResidence = sanitize($p_countryOfResidence);
$isUSCitizenOrPR = sanitize($isUSCitizenOrPR);
$reportedEthnicity = sanitize($reportedEthnicity);
$reportedGender = sanitize($reportedGender);
$currentUniversity = sanitize($currentUniversity);
$academicLevel = sanitize($academicLevel);
$expectedGradDate = sanitize($expectedGradDate);
$overallCollegeGPA = sanitize($overallCollegeGPA);
$overallHighSchoolGPA = sanitize($overallHighSchoolGPA);
$standardizedTestType = sanitize($standardizedTestType);
$standardizedTestScore = sanitize($standardizedTestScore);
$participateToLearn = sanitize($participateToLearn);
$participateForResume = sanitize($participateForResume);
$participateForMoney = sanitize($participateForMoney);
$participateForNetworking = sanitize($participateForNetworking);
$participateForOther = sanitize($participateForOther);
$participateForOtherText = sanitize($participateForOtherText);
$goalGradSchool = sanitize($goalGradSchool);
$goalWorkIndustry = sanitize($goalWorkIndustry);
$goalWorkLab = sanitize($goalWorkLab);
$goalWorkOther = sanitize($goalWorkOther);
$goalWorkOtherText = sanitize($goalWorkOtherText);
$whatIsDreamJob = sanitize($whatIsDreamJob);
$familiarityC = sanitize($familiarityC);
$familiarityJava = sanitize($familiarityJava);
$familiarityPython = sanitize($familiarityPython);
$familiarityMATLAB = sanitize($familiarityMATLAB);
$familiarityR = sanitize($familiarityR);
$coursesTaken = sanitize($coursesTaken);
$awardsOrHonors = sanitize($awardsOrHonors);
$rankGenomics = sanitize($rankGenomics);
$rankEHR = sanitize($rankEHR);
$rankMachineLearning = sanitize($rankMachineLearning);
$rankDataMining = sanitize($rankDataMining);
$referenceOneFirstName = sanitize($referenceOneFirstName);
$referenceOneLastName = sanitize($referenceOneLastName);
$referenceOneTitle = sanitize($referenceOneTitle);
$referenceOneRelationship = sanitize($referenceOneRelationship);
$referenceOneInstitution = sanitize($referenceOneInstitution);
$referenceOneStreetAddress = sanitize($referenceOneStreetAddress);
$referenceOneCityOfResidence = sanitize($referenceOneCityOfResidence);
$referenceOneStateProvinceRegion = sanitize($referenceOneStateProvinceRegion);
$referenceOneZipOrPostcode = sanitize($referenceOneZipOrPostcode);
$referenceOneCountryOfResidence = sanitize($referenceOneCountryOfResidence);
$referenceOnePhoneNumber = sanitize($referenceOnePhoneNumber);
$referenceOneEMailAddress = sanitize($referenceOneEMailAddress);
$isSubmittingSecondReference = sanitize($isSubmittingSecondReference);
$referenceTwoFirstName = sanitize($referenceTwoFirstName);
$referenceTwoLastName = sanitize($referenceTwoLastName);
$referenceTwoTitle = sanitize($referenceTwoTitle);
$referenceTwoRelationship = sanitize($referenceTwoRelationship);
$referenceTwoInstitution = sanitize($referenceTwoInstitution);
$referenceTwoStreetAddress = sanitize($referenceTwoStreetAddress);
$referenceTwoCityOfResidence = sanitize($referenceTwoCityOfResidence);
$referenceTwoStateProvinceRegion = sanitize($referenceTwoStateProvinceRegion);
$referenceTwoZipOrPostcode = sanitize($referenceTwoZipOrPostcode);
$referenceTwoCountryOfResidence = sanitize($referenceTwoCountryOfResidence);
$referenceTwoPhoneNumber = sanitize($referenceTwoPhoneNumber);
$referenceTwoEMailAddress = sanitize($referenceTwoEMailAddress);
$uploadPersonalStatement = sanitize($uploadPersonalStatement);
$personalStatementFile = sanitize($personalStatementFile);
$cvOrResumeFile = sanitize($cvOrResumeFile);
$personalStatement = sanitize($personalStatement);
$cvOrResume = sanitize($cvOrResume);
$mailLetterOfRec = sanitize($mailLetterOfRec);
$mailUnofficialTrans = sanitize($mailUnofficialTrans);
$unofficialTransFile = sanitize($unofficialTransFile);
$foundOutProfAtOwnUni = sanitize($foundOutProfAtOwnUni);
$foundOutWebSearch = sanitize($foundOutWebSearch);
$foundOutPastParticipant = sanitize($foundOutPastParticipant);
$foundOutAdvertisment = sanitize($foundOutAdvertisment);
$foundOutOther = sanitize($foundOutOther);
$foundOutOtherText = sanitize($foundOutOtherText);

print LOGFILE "sanitized personal statement file: " . $personalStatementFile . "\n";
print LOGFILE "sanitized unofficial transcript file: " . $unofficialTransFile . "\n";
print LOGFILE "sanitized cv or resume file: " . $cvOrResumeFile . "\n";

# Now perform input validation.
#  * The process of removing invalid characters should have been done by sanitize()
#     above.
#  * Here we are mostly catching (1) fields where the input size is out of bounds and
#  *  (2) business logic errors in filling out the form.

# 1. first name out of bounds
if ((length($firstName) < 1) || (length($firstName) > 254)) {
    handleInputError(1);
}

# 2. last name out of bounds
if ((length($lastName) < 1) || (length($lastName) > 254)) {
    handleInputError(2);
}

# 3. date of birth out of bounds
if ((length($dateOfBirth) < 1) || (length($dateOfBirth) > 254)) {
    handleInputError(3);
}

# 4. e-mail address out of bounds
if ((length($eMailAddress) < 1) || (length($eMailAddress) > 254)) {
    handleInputError(4);
}

# 5. phone number out of bounds
if ((length($phoneNumber) < 1) || (length($phoneNumber) > 254)) {
    handleInputError(5);
}

# 6. street address out of bounds
if ((length($streetAddress) < 1) || (length($streetAddress) > 254)) {
    handleInputError(6);
}

# 7. city out of bounds
if ((length($cityOfResidence) < 1) || (length($cityOfResidence) > 254)) {
    handleInputError(7);
}

# 8. state/province/region out of bounds
if ((length($stateProvinceRegion) < 1) || (length($stateProvinceRegion) > 254)) {
    handleInputError(8);
}

# 9. zip/postcode out of bounds
if ((length($zipOrPostcode) < 1) || (length($zipOrPostcode) > 254)) {
    handleInputError(9);
}

# 41. Permanent address ambiguous (neither is set)
if ($isPermanentAddress == 9) {
    handleInputError(41);
}

# 10. isPermAddress=0/false AND p_streetaddress out of bounds
if (($isPermanentAddress == 0) && ((length($p_streetAddress) < 1) || (length($p_streetAddress) > 254))) {
    handleInputError(10);
}

# 11. isPermAddress=0/false AND p_cityofresidence out of bounds
if (($isPermanentAddress == 0) && ((length($p_cityOfResidence) < 1) || (length($p_cityOfResidence) > 254))) {
    handleInputError(11);
}

# 12. isPermAddress=0/false AND p_state out of bounds
if (($isPermanentAddress == 0) && ((length($p_stateProvinceRegion) < 1) || (length($p_stateProvinceRegion) > 254))) {
    handleInputError(12);
}

# 13. isPermAddress=0/false AND p_zip out of bounds
if (($isPermanentAddress == 0) && ((length($p_zipOrPostcode) < 1) || (length($p_zipOrPostcode) > 254))) {
    handleInputError(13);
}

# 14. isUSCitizenOrPR is ambiguous (neither is set)
if ($isUSCitizenOrPR == 9) {
    handleInputError(14);
}

# 42. no ethnicity specified
if ($reportedEthnicity eq "Please choose") {
    handleInputError(42);
}

# 15. reportedGender is ambiguous (neither is set)
if ($reportedGender == 9) {
    handleInputError(15);
}

# 16. current university/college out of bounds
if ((length($currentUniversity) < 1) || (length($currentUniversity) > 254)) {
    handleInputError(16);
}

# 17. date degree expected out of bounds
if ((length($expectedGradDate) < 1) || (length($expectedGradDate) > 254)) {
    handleInputError(17);
}

# 18. college  GPA out of bounds
if ((length($overallCollegeGPA) < 1) || (length($overallCollegeGPA) > 254)) {
    handleInputError(18);
}

# 60. high school gpa out of bounds
if ((length($overallHighSchoolGPA) < 1) || (length($overallHighSchoolGPA) > 254)) {
    handleInputError(60);
}

# 61. standardized test score out of bounds
if ((length($standardizedTestScore) < 1) || (length($standardizedTestScore) > 254)) {
    handleInputError(61);
}

# 19. courses taken out of bounds
if ((length($coursesTaken) < 1) || (length($coursesTaken) > 8192)) {
    handleInputError(19);
}

# 20. awards/honors out of bounds
if ((length($awardsOrHonors) < 1) || (length($awardsOrHonors) > 8192)) {
    handleInputError(20);
}

# 62. no want to participate checked
if (($participateToLearn eq "") && ($participateForResume eq "") && ($participateForMoney eq "") && ($participateForNetworking eq "") && ($participateForOther eq "")) {
    handleInputError(62);
}

# 63. no goals checked
if (($goalGradSchool eq "") && ($goalWorkIndustry eq "") && ($goalWorkLab eq "") && ($goalWorkOther eq "")) {
    handleInputError(63);
}

# 64. dream job out of bounds
if ((length($whatIsDreamJob) < 1) || (length($whatIsDreamJob) > 8192)) {
    handleInputError(64);
}

# 65. no C familiarity set
if ($familiarityC == 9) {
    handleInputError(65);
}

# 66. no java familiarity set
if ($familiarityJava == 9) {
    handleInputError(66);
}

# 67. no python familiarity set
if ($familiarityPython == 9) {
    handleInputError(67);
}

# 68. no matlab familiarity set
if ($familiarityMATLAB == 9) {
    handleInputError(68);
}

# 69. no R familiarity set
if ($familiarityR == 9) {
    handleInputError(69);
}

# 70. file error with the resume or cv
if (!$cvOrResumeFile) {
    handleInputError(70);
}

# 71. no promotional mechanism specified
if (($foundOutProfAtOwnUni eq "") && ($foundOutWebSearch eq "") && ($foundOutPastParticipant eq "") && ($foundOutAdvertisment eq "") && ($foundOutOther eq "")) {
    handleInputError(71);
}

# 43. no explicit setting for personal statement
if ($uploadPersonalStatement == 9) {
    handleInputError(43)
}

# 21. no explicit setting for rankGenomics
if ($rankGenomics == 9) {
    handleInputError(21);
}

# 23. no explicit setting for rankEHR
if ($rankEHR == 9) {
    handleInputError(23);
}

# 47. no explicit setting for rankML
if ($rankMachineLearning == 9) {
    handleInputError(47);
}

# 48. no explicit setting for rankDM
if ($rankDataMining == 9) {
    handleInputError(48);
}

# 24. contradictory ranking of the sub-programs
if (($rankGenomics == $rankEHR) || ($rankGenomics == $rankMachineLearning) || ($rankGenomics == $rankDataMining) || ($rankEHR == $rankGenomics) || ($rankEHR == $rankMachineLearning) || ($rankEHR == $rankDataMining) || ($rankMachineLearning == $rankGenomics) || ($rankMachineLearning == $rankEHR) || ($rankMachineLearning == $rankDataMining) || ($rankDataMining == $rankGenomics) || ($rankDataMining == $rankEHR) || ($rankDataMining == $rankMachineLearning)) {
    handleInputError(24);
}

# 25. reference 1 first name out of bounds
if ((length($referenceOneFirstName) < 1) || (length($referenceOneFirstName) > 254)) {
    handleInputError(25);
}

# 26. reference 1 last name out of bounds
if ((length($referenceOneLastName) < 1) || (length($referenceOneLastName) > 254)) {
    handleInputError(26);
}

# 27. reference 1 title out of bounds
if ((length($referenceOneTitle) < 1) || (length($referenceOneTitle) > 254)) {
    handleInputError(27);
}

# 28. reference 1 relationship out of bounds
if ((length($referenceOneRelationship) < 1) || (length($referenceOneRelationship) > 254)) {
    handleInputError(27);
}

# 29. reference 1 institution out of bounds
if ((length($referenceOneInstitution) < 1) || (length($referenceOneInstitution) > 254)) {
    handleInputError(29);
}

# 30. reference 1 street address out of bounds
if ((length($referenceOneStreetAddress) < 1) || (length($referenceOneStreetAddress) > 254)) {
    handleInputError(30);
}

# 31. reference 1 city out of bounds
if ((length($referenceOneCityOfResidence) < 1) || (length($referenceOneCityOfResidence) > 254)) {
    handleInputError(31);
}

# 32. reference 1 state/province/region out of bounds
if ((length($referenceOneStateProvinceRegion) < 1) || (length($referenceOneStateProvinceRegion) > 254)) {
    handleInputError(32);
}

# 33. reference 1 zip/postcode out of bounds
if ((length($referenceOneZipOrPostcode) < 1) || (length($referenceOneZipOrPostcode) > 254)) {
    handleInputError(33);
}

# 34. reference 1 phone number out of bounds
if ((length($referenceOnePhoneNumber) < 1) || (length($referenceOnePhoneNumber) > 254)) {
    handleInputError(34);
}

# 35. reference 1 e-mail address out of bounds
if ((length($referenceOneEMailAddress) < 1) || (length($referenceOneEMailAddress) > 254)) {
    handleInputError(35);
}

# 49-59. second reference errors
if ($isSubmittingSecondReference eq "on") {
    # 49. reference 2 first name out of bounds
    if ((length($referenceOneFirstName) < 1) || (length($referenceOneFirstName) > 254)) {
        handleInputError(49);
    }

    # 50. reference 2 last name out of bounds
    if ((length($referenceOneLastName) < 1) || (length($referenceOneLastName) > 254)) {
        handleInputError(50);
    }

    # 51. reference 2 title out of bounds
    if ((length($referenceOneTitle) < 1) || (length($referenceOneTitle) > 254)) {
        handleInputError(51);
    }

    # 52. reference 2 relationship out of bounds
    if ((length($referenceOneRelationship) < 1) || (length($referenceOneRelationship) > 254)) {
        handleInputError(52);
    }

    # 53. reference 2 institution out of bounds
    if ((length($referenceOneInstitution) < 1) || (length($referenceOneInstitution) > 254)) {
        handleInputError(53);
    }

    # 54. reference 2 street address out of bounds
    if ((length($referenceOneStreetAddress) < 1) || (length($referenceOneStreetAddress) > 254)) {
        handleInputError(54);
    }

    # 55. reference 2 city out of bounds
    if ((length($referenceOneCityOfResidence) < 1) || (length($referenceOneCityOfResidence) > 254)) {
        handleInputError(55);
    }

    # 56. reference 2 state/province/region out of bounds
    if ((length($referenceOneStateProvinceRegion) < 1) || (length($referenceOneStateProvinceRegion) > 254)) {
        handleInputError(56);
    }

    # 57. reference 2 zip/postcode out of bounds
    if ((length($referenceOneZipOrPostcode) < 1) || (length($referenceOneZipOrPostcode) > 254)) {
        handleInputError(57);
    }

    # 58. reference 2 phone number out of bounds
    if ((length($referenceOnePhoneNumber) < 1) || (length($referenceOnePhoneNumber) > 254)) {
        handleInputError(58);
    }

    # 59. reference 2 e-mail address out of bounds
    if ((length($referenceOneEMailAddress) < 1) || (length($referenceOneEMailAddress) > 254)) {
        handleInputError(59);
    }
}
# 36. uploadPersonalStatement set to 1/true AND any file problem
if (($uploadPersonalStatement == 1) && !$personalStatementFile) {
    handleInputError(36);
}

# 37. uploadPersonalStatement set to 0/false (text box) AND  text box out of bounds
if (($uploadPersonalStatement == 0) && ((length($personalStatement) < 1) || (length($personalStatement) > 8192))) {
    handleInputError(37);
}

# 38. no explicit setting for mailLetterOfRec
if ($mailLetterOfRec == 9) {
    handleInputError(38);
}

# 39. no explicit setting for mailUnofficialTrans
if ($mailUnofficialTrans == 9) {
    handleInputError(39);
}

# 40. mailUnofficialTrans set to false/upload AND any file problem 
if (($mailUnofficialTrans == 0) && !$unofficialTransFile) {
    handleInputError(40);
}

#46. howFindOutAbout was specified, but is out of bounds
if (($howFindOutAbout ne "") && (length($howFindOutAbout) > 1023)) {
    handleInputError(46);
}

# Filler for blank fields when personal address is permanent address.
if ($isPermanentAddress == 1) {
    $p_streetAddress = "N/A";
    $p_cityOfResidence = "N/A";
    $p_stateProvinceRegion = "N/A";
    $p_zipOrPostcode = "N/A";
    $p_countryOfResidence = "N/A";
}

# Filler for blank fields when only one reference is specified.
if ($isSubmittingSecondReference ne "on") {
    $referenceTwoFirstName = "N/A";
    $referenceTwoLastName = "N/A";
    $referenceTwoTitle = "N/A";
    $referenceTwoRelationship = "N/A";
    $referenceTwoInstitution = "N/A";
    $referenceTwoStreetAddress = "N/A";
    $referenceTwoCityOfResidence = "N/A";
    $referenceTwoStateProvinceRegion = "N/A";
    $referenceTwoZipOrPostcode = "N/A";
    $referenceTwoCountryOfResidence = "N/A";
    $referenceTwoPhoneNumber = "N/A";
    $referenceTwoEMailAddress = "N/A";
}

# Filler for blank fields when personal statement is set to upload from file.
if ($uploadPersonalStatement == 1) {
    $personalStatement = "N/A";
}

# Check for duplicate registration.
# There are many ways we could do this but keying simply off the e-mail address seems
#  to work well.
$db_query = "SELECT * FROM registrations where eMailAddress = " . "\'" . $eMailAddress . "\';";
$sth = $dbh->prepare($db_query);
$sth->execute;

$result = eval { $sth->fetchrow_arrayref->[1] };

# If we get any results back at all, we know that the registration is a
# duplicate.

if ($result) {
    handleDuplicateRegistration();
}

# If this event will have some limit on the number of registrants, uncomment the code
#  below to enable support for catching that.

#$db_query = "SELECT COUNT(*) FROM registrations";
#$sth = $dbh->prepare($db_query);
#$sth->execute;
#
#$totalrows = $sth->fetchrow_array;
#
#if ( $totalrows >= 270 ) {
#	handleTooManyRegistrations();
#}

# Handle determining an anonymized name for the personal statement file as well as the
#  actual upload of the file.
# Note that for file uploads to work properly, the enctype="multipart/form-data" parameter
#  must be specified in the HTML form definition.
# This is just fixed at one now, I guess we used to allow people the option to
#  type the personal statement in a textbox on the page but now we only permit
#  file uploads.
if ( $uploadPersonalStatement == 1 ) {
    $posn = -1;

    # Determine name and extension of uploaded file
    for ( $i = 0; $i < length($personalStatementFile); $i++ ) {
        $ss = substr($personalStatementFile, $i, 1);

        if ($ss eq ".") {
                $posn = $i;
        }
    }

    # Check for no file type extension
    if ( $posn == -1 ) {
        handleInputError(44);
    }

    $name = substr($personalStatementFile, 0, $posn);
    $extension = substr($personalStatementFile, $posn, length($personalStatementFile) );

    $newPersonalStatementFile = md5_hex($name . time) . $extension;

    # determine URL for the personal statement
    $newPersonalStatementURL = "http://bigdatasummerinst.sph.umich.edu/uploads/" . $newPersonalStatementFile;

    # Grab the filehandle for the uploaded file
    $upload_filehandle = $query->upload("personalStatementFile");

    print LOGFILE "trying to write personal statement to: " . $uploadDir . "/" . $newPersonalStatementFile . "\n";

    # Write the file out to local disk
    open UPLOADFILE, ">$uploadDir/$newPersonalStatementFile";
    binmode UPLOADFILE;
    while (<$upload_filehandle>) {
        print UPLOADFILE;
    }

    close UPLOADFILE;
}

# Handle determining an anonymized name for the unofficial transcript file as well as the
#  actual upload of the file.
# Note that for file uploads to work properly, the enctype="multipart/form-data" parameter
#  must be specified in the HTML form definition.
if ( $mailUnofficialTrans == 0 ) {
    $posn = -1;

    # Determine name and extension of uploaded file
    for ( $i = 0; $i < length($unofficialTransFile); $i++ ) {
        $ss = substr($unofficialTransFile, $i, 1);

        if ($ss eq ".") {
            $posn = $i;
        }
    }

    # Check for no file type extension
    if ( $posn == -1 ) {
        handleInputError(45);
    }

    $name = substr($unofficialTransFile, 0, $posn);
    $extension = substr($unofficialTransFile, $posn, length($unofficialTransFile) );

    $newUnofficialTransFile = md5_hex($name . time) . $extension;

    # determine URL for the personal statement
    $newUnofficialTransURL = "http://bigdatasummerinst.sph.umich.edu/uploads/" . $newUnofficialTransFile;

    # Grab the filehandle for the uploaded file
    $upload_filehandle = $query->upload("unofficialTransFile");

    print LOGFILE "trying to write unofficial transcript to: " . $uploadDir . "/" . $newUnofficialTransFile . "\n";

    # Write the file out to local disk
    open UPLOADFILE, ">$uploadDir/$newUnofficialTransFile";
    binmode UPLOADFILE;
    while (<$upload_filehandle>) {
        print UPLOADFILE;
    }

    close UPLOADFILE;
}

# Handle determining an anonymized file name for the CV or resume
#  As always, for file uploads to work properly, we need enctype="multipart/form-data"

$posn = -1;

# Determine name and extension of uploaded file
for ( $i = 0; $i < length($cvOrResumeFile); $i++ ) {
    $ss = substr($cvOrResumeFile, $i, 1);

    if ($ss eq ".") {
        $posn = $i;
    }
}

# Check for no file type extension
if ( $posn == -1 ) {
    handleInputError(46);
}

$name = substr($cvOrResumeFile, 0, $posn);

$extension = substr($cvOrResumeFile, $posn, length(cvOrResumeFile) );
$newCvOrResumeFile = md5_hex($name . time) . $extension;

# determine URL for the CV or resume
$newCvOrResumeURL = "http://bigdatasummerinst.sph.umich.edu/uploads/" . $newCvOrResumeFile;

# Grab the filehandle for the uploaded file
$upload_filehandle = $query->upload("cvOrResumeFile");

print LOGFILE "trying to write personal statement to: " . $uploadDir . "/" . $newCvOrResumeURL . "\n";

# Write the file out to local disk
open UPLOADFILE, ">$uploadDir/$newCvOrResumeFile";
binmode UPLOADFILE;
while (<$upload_filehandle>) {
    print UPLOADFILE;
}

close UPLOADFILE;

# Determine order number (basically a serial number for every registration that we record).
# The query needs to return in ascending order otherwise we can't properly find the last
#  previous order number.
$db_query = "SELECT * FROM registrations ORDER BY orderNumber ASC;";
$sth = $dbh->prepare($db_query);
$sth->execute;

@result = $sth->fetchrow_array;

# If no records in table, this is our first order, order number is 1.
if ( scalar @result == 0) {
    $orderNumber = 1;
}

# Otherwise order number = last order number + 1.
else {
    # iterate over all rows until we find the last order number
    # then order number = last order number + 1

    do {
        $lastOrderNumber = @result[0];

        @result = $sth->fetchrow_array;

    } while (scalar @result != 0);

    $orderNumber = $lastOrderNumber + 1;
}

# If the event is charged for and there is some form field that might set a variable cost
#  uncomment the following code below to add support for handling that (and update your
#  schema).

#if ( $isStudent eq 'true' ) {
#	$totalCost = 50;
#}
#else {
#	$totalCost = 125;
#}

# Construct an insert command to dump the registration into the database.
$db_query = "INSERT INTO registrations VALUES ( " . $orderNumber . ", now(), " . "\'" . $firstName . "\', \'" . $lastName . "\', \'" . $dateOfBirth . "\', \'" . $eMailAddress . "\', \'" . $phoneNumber . "\', \'" . $streetAddress ."\', \'" . $cityOfResidence . "\', \'" . $stateProvinceRegion . "\', \'" . $zipOrPostcode . "\', \'" . $countryOfResidence . "\', " . $isPermanentAddress . ", \'" . $p_streetAddress . "\', \'" . $p_cityOfResidence . "\', \'" . $p_stateProvinceRegion . "\', \'" . $p_zipOrPostcode . "\', \'" . $p_countryOfResidence . "\', " . $isUSCitizenOrPR . ", \'" . $reportedEthnicity . "\', " . $reportedGender . ", \'" . $currentUniversity . "\', \'" . $academicLevel . "\', \'" . $expectedGradDate . "\', \'" . $overallCollegeGPA . "\', \'" . $overallHighSchoolGPA . "\', \'" . $standardizedTestType . "\', \'" . $standardizedTestScore . "\', \'" . $participateToLearn . "\', \'" . $participateForResume . "\', \'" . $participateForMoney . "\', \'" . $participateForNetworking . "\', \'" . $participateForOther . "\', \'" . $participateForOtherText . "\', \'" . $goalGradSchool . "\', \'" . $goalWorkIndustry . "\', \'" . $goalWorkLab . "\', \'" . $goalWorkOther . "\', \'" . $goalWorkOtherText . "\', \'" . $whatIsDreamJob . "\', " . $familiarityC . ", " . $familiarityJava . ", " . $familiarityPython . ", " . $familiarityMATLAB . ", " . $familiarityR . ", \'" . $coursesTaken . "\', \'" . $awardsOrHonors . "\', " . $rankGenomics . ", " . $rankEHR . ", " . $rankMachineLearning . ", " . $rankDataMining . ", \'" . $referenceOneFirstName . "\', \'" . $referenceOneLastName . "\', \'" . $referenceOneTitle . "\', \'" . $referenceOneRelationship . "\', \'" . $referenceOneInstitution . "\', \'" . $referenceOneStreetAddress . "\', \'" . $referenceOneCityOfResidence . "\', \'" . $referenceOneStateProvinceRegion . "\', \'" . $referenceOneZipOrPostcode . "\', \'" . $referenceOneCountryOfResidence . "\', \'" . $referenceOnePhoneNumber . "\', \'" . $referenceOneEMailAddress . "\', \'" .$isSubmittingSecondReference . "\', \'" . $referenceTwoFirstName . "\', \'" . $referenceTwoLastName . "\', \'" . $referenceTwoTitle . "\', \'" . $referenceTwoRelationship . "\', \'" . $referenceTwoInstitution . "\', \'" . $referenceTwoStreetAddress . "\', \'" . $referenceTwoCityOfResidence . "\', \'" . $referenceTwoStateProvinceRegion . "\', \'" . $referenceTwoZipOrPostcode . "\', \'" . $referenceTwoCountryOfResidence . "\', \'" . $referenceTwoPhoneNumber . "\', \'" . $referenceTwoEMailAddress . "\', " . $uploadPersonalStatement . ",\'" . $newPersonalStatementURL . "\', \'" .$newCvOrResumeURL . "\', \'" . $personalStatement . "\', \'" . $cvOrResume . "\'," . $mailLetterOfRec . "," . $mailUnofficialTrans . ",\'" . $newUnofficialTransURL . "\', \'" . $foundOutProfAtOwnUni . "\', \'" . $foundOutWebSearch . "\', \'" . $foundOutPastParticipant . "\', \'" . $foundOutAdvertisment . "\', \'" . $foundOutOther . "\', \'" . $foundOutOtherText .  "\' );";

print LOGFILE "\n" . $db_query . "\n";

# Actually execute the statement to insert the record into the database.
$sth = $dbh->prepare($db_query);
$sth->execute;

# generate and show registration complete page + route to nelnet
#  - embed order number, cost in nelnet URL generated and inserted into
#    page.

# Time needs to be expressed in milliseconds for Nelnet.
#$timeStamp = time * 1000;

# Set this to whatever the Nelnet people tell us to use.
#$orderType="Michigan Genomics";

# Read in Nelnet password.
#open NELNETKEYFILE, "</etc/apache2/nelnetkey.registrations";
#$keyString = <NELNETKEYFILE>;
#close NELNETKEYFILE;
#chomp $keyString;

# Convert totalCost (aka amountDue) to cents for nelnet
#$totalCost = $totalCost * 100;

# Nelnet documentation says orderType comes before orderNumber, but in the errata
# orderNumber comes prior to orderType and THIS IS WHAT MUST BE DONE FOR IT TO WORK.
# amountDue is totalCost
#$tempHashInput = $orderNumber.$orderType.$totalCost.$timeStamp.$keyString;

# Be sure to use md5_hex() and not md5() to calculate the hash.
#$hashVal = md5_hex($tempHashInput);

# Write out the page to inform the registrant that all their data has been taken
# and that registration is complete.
print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Application Complete</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
The application process is complete. You should receive an e-mail soon to confirm your application.
<p>
</center>
</body>
</html>
END

# Send registration confirmation e-mail to the applicant with the text supplied by Bhramar.
$bhramarEmail = "bhramar\@umich.edu";
$sabrinaEmail = "siclayto\@umich.edu";

$smtp = Net::SMTP->new("localhost");

$smtp->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp->recipient($eMailAddress, $sabrinaEmail);

$smtp->data();
$smtp->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu\n");
$smtp->datasend("To: " . $eMailAddress . "\n");
$smtp->datasend("CC: " . $sabrinaEmail . "\n");
$smtp->datasend("Subject: University of Michigan Summer Institute in Biostatistics, submission of application confirmation\n");
$smtp->datasend("\n");
$smtp->datasend("Dear $firstName $lastName,\n\n");
$smtp->datasend("Thank you for submitting your application to the University of Michigan, Department of Biostatistics, School of Public Health Summer Institute, Transforming Analytical Learning in the Era of Big Data: A Summer Institute in Biostatistics, June 13-July 22, 2016.\n\n");
$smtp->datasend("We will evaluate the applications on a rolling basis and notify you by e-mail as soon as the decision is reached, no later than March 31, 2016.\n\n");
#$smtp->datasend("Thank you for your interest in the pilot offering of the program. If you have any further questions please feel free to contact us via e-mail.\n\n");
$smtp->datasend("Best wishes,\n\n");
$smtp->datasend("Bhramar Mukherjee\nJohn D Kalbfleisch Collegiate Professor of Biostatistics\nAssociate Chair of Biostatistics\nProfessor of Epidemiology\n");
$smtp->datasend("School of Public Health\n");
$smtp->datasend("University of Michigan\n1415 Washington Heights, SPH II\nAnn Arbor, MI 48109\n\n");
$smtp->datasend("Phone: (734) 764-6544\nFAX: (734) 763-2215\nE-mail: bhramar\@umich.edu\n");
$smtp->datasend("Webpage: http://www-personal.umich.edu/~bhramar\n\n");

$smtp->dataend();
$smtp->quit;

# Send e-mail soliciting letter of recommendation to the reference supplied in the form.
$smtp_2 = Net::SMTP->new("localhost");

$smtp_2->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp_2->recipient($referenceOneEMailAddress, $sabrinaEmail);

$smtp_2->data();
$smtp_2->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu\n");
$smtp_2->datasend("To: " . $referenceOneEMailAddress . "\n");
$smtp_2->datasend("CC: " . $sabrinaEmail . "\n"); 
$smtp_2->datasend("Subject: University of Michigan Summer Institute in Biostatistics Letter of Recommendation Request\n");
$smtp_2->datasend("\n");

$smtp_2->datasend("Dear Professor $referenceOneLastName,\n\n");
$smtp_2->datasend("Thank you for agreeing to submit a letter of recommendation in support of $firstName ${lastName}'s application to the University of Michigan, Department of Biostatistics, School of Public Health Summer Research Institute, Transforming Analytical Learning in the Era of Big Data: A Summer Institute in Biostatistics, June 13-July 22, 2016.\n\n");
$smtp_2->datasend("Your letter of recommendation is due by March 15, 2016.\n\n");
$smtp_2->datasend("Please e-mail an electronic copy of your letter or mail it to:\n\n");
$smtp_2->datasend("Sabrina Clayton\n");
$smtp_2->datasend("School of Public Health, University of Michigan\n");
$smtp_2->datasend("1415 Washington Heights, SPH II\nAnn Arbor, MI 48109\nPhone: (734) 764-5450\n");
$smtp_2->datasend("FAX: (734) 763-2215\nE-mail: siclayto\@umich.edu\n\n");
$smtp_2->datasend("Thank you,\n\n");
$smtp->datasend("Bhramar Mukherjee\nJohn D Kalbfleisch Collegiate Professor of Biostatistics\nAssociate Chair of Biostatistics\nProfessor of Epidemiology\n");
$smtp->datasend("School of Public Health\n");
$smtp->datasend("University of Michigan\n1415 Washington Heights, SPH II\nAnn Arbor, MI 48109\n\n");
$smtp->datasend("Phone: (734) 764-6544\nFAX: (734) 763-2215\nE-mail: bhramar\@umich.edu\n");
$smtp->datasend("Webpage: http://www-personal.umich.edu/~bhramar\n\n");

$smtp_2->dataend();
$smtp_2->quit;

# If they provided a second reference, we have to generate a second solicitation e-mail.
if (isSubmittingSecondReference eq "on" ) {
$smtp_3 = Net::SMTP->new("localhost");

$smtp_3->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp_3->recipient($referenceTwoMailAddress, $sabrinaEmail);

$smtp_3->data();
$smtp_3->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu\n");
$smtp_3->datasend("To: " . $referenceTwoEMailAddress . "\n");
$smtp_3->datasend("CC: " . $sabrinaEmail . "\n");
$smtp_3->datasend("Subject: University of Michigan Summer Institute in Biostatistics Letter of Recommendation Request\n");
$smtp_3->datasend("\n");

$smtp_3->datasend("Dear Professor $referenceTwoLastName,\n\n");
$smtp_3->datasend("Thank you for agreeing to submit a letter of recommendation in support of $firstname ${lastName}'s application to the University of Michigan, Department of Biostatistics, School of Public Health Summer Research Institute, Transforming Analytical Learning in the Era of Big Data: A Summer Institute in Biostatistics, June 13-July 22, 2016.\n\n");
$smtp_3->datasend("Your letter of recommendation is due by March 15, 2016.\n\n");
$smtp_3->datasend("Please e-mail an electronic copy of your letter or mail it to:\n\n");
$smtp_3->datasend("Sabrina Clayton\n");
$smtp_3->datasend("School of Public Health, University of Michigan\n");
$smtp_3->datasend("1415 Washington Heights, SPH II\nAnn Arbor, MI 48109\nPhone: (734) 764-5450\n");
$smtp_3->datasend("FAX: (734) 763-2215\nE-mail: siclayto\@umich.edu\n\n");
$smtp_3->datasend("Thank you,\n\n");
$smtp->datasend("Bhramar Mukherjee\nJohn D Kalbfleisch Collegiate Professor of Biostatistics\nAssociate Chair of Biostatistics\nProfessor of Epidemiology\n");
$smtp->datasend("School of Public Health\n");
$smtp->datasend("University of Michigan\n1415 Washington Heights, SPH II\nAnn Arbor, MI 48109\n\n");
$smtp->datasend("Phone: (734) 764-6544\nFAX: (734) 763-2215\nE-mail: bhramar\@umich.edu\n");
$smtp->datasend("Webpage: http://www-personal.umich.edu/~bhramar\n\n");

$smtp_3->dataend();
$smtp_3->quit;

}

# Send e-mail to Bhramar to notify of incoming registration.
#$smtp_3 = Net::SMTP->new("localhost");

#$smtp_3->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
#$smtp_3->recipient("bhramar\@umich.edu");

#$smtp_3->data();
#$smtp_3->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu");
#$smtp_3->datasend("To: bhramar\@umich.edu\n");
#$smtp_3->datasend("Subject: U-M Summer Institute in Biostatistics New Registration Notification\n");
#$smtp_3->datasend("\n");
#$smtp_3->datasend("A new registration has been entered into the system. Please review when convenient.\n\n");
#$smtp_3->datasend("As a reminder, the URL used to review incoming registrations is as follows.\n\n");
#$smtp_3->datasend("http://bigdatasummerinst.sph.umich.edu/cgi-bin/admin/admin.cgi\n\n");
#$smtp_3->dataend();

#$smtp_3->quit;

# Send e-mail to Sabrina to notify of incoming registration.
$smtp_4 = Net::SMTP->new("localhost");

$smtp_4->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp_4->recipient("siclayto\@umich.edu");

$smtp_4->data();
$smtp_4->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp_4->datasend("To: siclayto\@umich.edu\n");
$smtp_4->datasend("Subject: U-M Summer Institute in Biostatistics New Registration Notification\n");
$smtp_4->datasend("\n");
$smtp_4->datasend("A new registration has been entered into the system. Please review when convenient.\n\n");
$smtp_4->datasend("As a reminder, the URL used to review incoming registrations is as follows\n\n");
$smtp_4->datasend("http://bigdatasummerinst.sph.umich.edu/cgi-bin/admin/admin.cgi\n\n");
$smtp_4->dataend();

$smtp_4->quit;

# Remember to close the logfile
close LOGFILE;

# Remember to disconnect from the database.
$dbh->disconnect();

# Script should terminate simply by running off the end here.

sub handleDuplicateRegistration {

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Duplicate Registration</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Someone has already applied for the summer course with the e-mail address that you supplied. Please confirm your application information and try again.
<p>
<form><input type="button" VALUE="Back" onCLick="history.go(-1);return true;"></form>
</center>
</body>
</html>
END

exit;
}

sub handleTooManyRegistrations {

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Registration Attendee Limit Reached</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Registration for the program is full. Please contact Sabrina Clayton at siclayto@umich.edu for further assistance.
<p>
<form><input type="button" VALUE="Back" onCLick="history.go(-1);return true;"></form>
</center>
</body>
</html>
END

exit;
}


sub handleInputError {
    $errorCode = @_[0];

    if ($errorCode == 1) {
        $errorText = "the first name field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 2) {
        $errorText = "the last name field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 3) {
        $errorText = "the date of birth field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 4) {
        $errorText = "the e-mail address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 5) {
        $errorText = "the phone number field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 6) {
        $errorText = "the street address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 7) {
        $errorText = "the city field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 8) {
        $errorText = "the state/province/region field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 9) {
        $errorText = "the ZIP/postcode field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 10) {
        $errorText = "the permanent street address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 11) {
        $errorText = "the permanent city address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 12) {
        $errorText = "the permanent state address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 13) {
        $errorText = "the permanent ZIP/postcode field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 14) {
        $errorText = "your US citizen or permanent resident status was not specified";
    }

    elsif ($errorCode == 15) {
        $errorText = "your gender was not specified";
    }

    elsif ($errorCode == 16) {
        $errorText = "the current university/college field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 17) {
        $errorText = "the date degree expected field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 18) {
        $errorText = "the college GPA field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 19) {
        $errorText = "the courses taken field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 20) {
        $errorText = "the awards/honors field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 21) {
        $errorText = "your genomics preference was not set";
    }

    elsif ($errorCode == 23) {
        $errorText = "your electronic health records preference was not set";
    }

    elsif ($errorCode == 24) {
        $errorText = "conflicting project area preferences were set.<p>Please set one area to 1, one area to 2, one area to 3 and one area to 4";
    }

    elsif ($errorCode == 25) {
        $errorText = "the first reference first name field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 26) {
        $errorText = "the first reference last name field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 27) {
        $errorText = "the first reference title field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 28) {
        $errorText = "the first reference relationship field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 29) {
        $errorText = "the first reference institution field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 30) {
        $errorText = "the first reference street address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 31) {
        $errorText = "the first reference city address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 32) {
        $errorText = "the first reference state/province/region field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 33) {
        $errorText = "the first reference ZIP/postcode field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 34) {
        $errorText = "the first reference phone number field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 35) {
        $errorText = "the first reference e-mail field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 36) {
        $errorText = "a file error occurred when attempting to upload your personal statement";
    }

    elsif ($errorCode == 37) {
        $errorText = "personal statement was set to text box and was left blank or exceeded length limits";
    }

    elsif ($errorCode == 38) {
        $errorText = "the letter of reference preference was not set";
    }

    elsif ($errorCode == 39) {
        $errorText = "the unofficial transcript preference was not set";
    }

    elsif ($errorCode == 40) {
        $errorText = "unofficial transcript was set to upload and a file error occurred";
    }

    elsif ($errorCode == 41) {
        $errorText = "the permanent address button was not set ";
    }

    elsif ($errorCode == 42) {
        $errorText = "your ethnicity was not specified";
    }

    elsif ($errorCode == 43) {
        $errorText = "your personal statement preference was not set";
    }

    elsif ($errorCode == 44) {
        $errorText = "your personal statement file is missing an extension (i.e. .doc, .docx, .pdf, .txt)";
    }

    elsif ($errorCode == 45) {
        $errorText = "your unofficial transcript file is missing an extension (i.e. .doc, .docx, .pdf, .txt)";
    }

    elsif ($errorCode == 46) {
        $errorText = "your CV or resume file is missing an extension (i.e. .doc, .docx, .pdf, .txt)";
    }

    elsif ($errorCode == 47) {
        $errorText = "your machine learning preference was not set";
    }

    elsif ($errorCode == 48) {
        $errorText = "your data mining preference was not set";
    }

    elsif ($errorCode == 49) {
        $errorText = "the second reference first name field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 50) {
        $errorText = "the second reference last name field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 51) {
        $errorText = "the second reference title field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 52) {
        $errorText = "the second reference relationship field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 53) {
        $errorText = "the second reference institution field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 54) {
        $errorText = "the second reference street address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 55) {
        $errorText = "the second reference city address field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 56) {
        $errorText = "the second reference state/province/region field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 57) {
        $errorText = "the second reference ZIP/postcode field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 58) {
        $errorText = "the second reference phone number field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 59) {
        $errorText = "the second reference e-mail field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 60) {
        $errorText = "the high school GPA field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 61) {
        $errorText = "the standardized test score field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 62) {
        $errorText = "no reason for participating was checked";
    }

    elsif ($errorCode == 63) {
        $errorText = "no goals were checked";
    }

    elsif ($errorCode == 64) {
        $errorText = "the dream job field was left blank or exceeded length limits";
    }

    elsif ($errorCode == 65) {
        $errorText = "no C familiarity specified";
    }

    elsif ($errorCode == 66) {
        $errorText = "no Java familiarity specified";
    }

    elsif ($errorCode == 67) {
        $errorText = "no Python familiarity specified";
    }

    elsif ($errorCode == 68) {
        $errorText = "no MATLAB familiarity specified";
    }

    elsif ($errorCode == 69) {
        $errorText = "no R familiarity specified";
    }

    elsif ($errorCode == 70) {
        $errorText = "a file error occurred when attempting to upload your resume or CV";
    }

    elsif ($errorCode == 71) {
        $errorText = "you did not specify how you found out about the program ";
    }

    else {
        $errorText = "of an undefined error";
    }

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Application Error</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Your application could not be processed because $errorText ($errorCode).
<p>
Please check your application information and try again.
<p>
<form><input type="button" VALUE="Back" onCLick="history.go(-1);return true;"></form>
</center>
</body>
</html>
END

exit;

}

sub sanitize {
    $input = @_[0];

    # remove html coding

    $input =~ s/%2C/,/g;
    $input =~ s/%40/@/g;
    $input =~ s/%21/\!/g;
    $input =~ s/%0D%0A/\n/g;
    $input =~ s/%3C/</g;
    $input =~ s/%3E/>/g;
    $input =~ s/%2F/\//g;
    $input =~ s/%3D/=/g;
    $input =~ s/%22/\"/g;
    $input =~ s/%3A/:/g;
    $input =~ s/%3F/\?/g;
    $input =~ s/%27/\'/g;
    $input =~ s/%3B/\;/g;
    $input =~ s/%28/\(/g;
    $input =~ s/%29/\)/g;

    $input =~ s/%23/#/g;
    $input =~ s/%24/\$/g;
    $input =~ s/%25/%/g;
    $input =~ s/%26/&/g;
    $input =~ s/%2A/*/g;
    $input =~ s/%2B/+/g;
    $input =~ s/%2D/-/g;
    $input =~ s/%2E/./g;

    $input =~ s/%5B/[/g;
    $input =~ s/%5C/\\/g;
    $input =~ s/%5D/]/g;
    $input =~ s/%5E/^/g;
    $input =~ s/%5F/_/g;
    $input =~ s/%60/`/g;
    $input =~ s/%7B/{/g;
    $input =~ s/%7C/|/g;
    $input =~ s/%7D/}/g;
    $input =~ s/%7E/~/g;

    # remove frontticks and backticks and backslashes

    $input =~ s/\'//g;
    $input =~ s/`//g;
    $input =~ s/\\//g;

    # filter out plus signs used to encode whitespace

    $input =~ tr/+/ /;

    # we need to escape question marks because they get confused
    # by the database as wildcards. we will just turn them into
    # periods and hope nobody notices.

    $input =~ s/\?/./g;

    # return the sanitized string.

    return $input;
}
