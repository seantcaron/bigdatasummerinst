#!/usr/bin/perl

use DBI;
use DBD::mysql;
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

# Maximum upload file size of 50 MB
$CGI::POST_MAX = 1024 * $config->val('global', 'postmax');

# Construct data source name
$dsn = "DBI:$platform:$database:$host:$port";

# Connect to database

# PERL DBI CONNECT
$dbh = DBI->connect($dsn, $user, $pw);

# Get form input passed from the WWW server.
if ($ENV{'REQUEST_METHOD'} eq "GET") {
        $input = $ENV{'QUERY_STRING'};
}
else {
        $input = <STDIN>;
}

# Parse input
$selectedOrderNumber = -1;
@inputs = split("&", $input);

foreach $pair (@inputs) {
	($key, $value) = split("=", $pair);

	$value = sanitize($value);
	$key = sanitize($key);

	if ( $key eq 'selectedApplicant' ) {
		$selectedOrderNumber = $value;
	}
}

# --- Print detailed view of a single applicant ---

if ($selectedOrderNumber != -1) {

# determine total number of rows.

$query = "SELECT COUNT(*) FROM registrations";
$sth = $dbh->prepare($query);
$sth->execute;

$totalrows = $sth->fetchrow_array;

# determine order number

# this needs to be in ascending order otherwise we can't properly
# find the last previous order number.
$query = "SELECT * FROM registrations WHERE orderNumber = " . $selectedOrderNumber;
$sth = $dbh->prepare($query);
$sth->execute;

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Transforming Analytical Learning in the Era of Big Data: Administrator</title>
</head>
<body>
<center>
<h2>Transforming Analytical Learning in the Era of Big Data - Attendee Detail View</h2>
</center>
<p>
END

@result = $sth->fetchrow_array;

# Textify various parameters we coded in the database as binary integer values

if ( @result[12] == 0 ) {
	$isPermanentAddress_text = "no";
}
else {
	$isPermanentAddress_text = "yes";
}

if ( @result[18] == 0 ) {
	$isUSCitizenOrPR_text = "no";
}
else {
	$isUSCitizenOrPR_text = "yes";
}

if ( @result[20] == 0 ) {
	$reportedGender_text = "female";
}
else {
	$reportedGender_text = "male";
}

if ( @result[28] eq "on" ) {
	$participateToLearn = "yes";
}
else {
	$participateToLearn = "no";
}

if ( @result[29] eq "on" ) {
	$participateForResume = "yes";
}
else {
	$participateForResume = "no";
}

if ( @result[30] eq "on" ) {
	$participateForMoney = "yes"
}
else {
	$participateForMoney = "no";
}

if ( @result[31] eq "on" ) {
	$participateForNetworking = "yes";
}
else {
	$participateForNetworking = "no";
}

if ( @result[32] eq "on" ) {
	$participateForOther = "yes";
}
else {
	$participateForOther = "no";
}

if ( @result[34] eq "on" ) {
	$goalGrad = "yes";
}
else {
	$goalGrad = "no";
}

if ( @result[35] eq "on" ) {
	$goalIndustry = "yes";
}
else {
	$goalIndustry = "no";
}

if ( @result[36] eq "on" ) {
	$goalLab = "yes";
}
else {
	$goalLab = "no";
}

if ( @result[37] eq "on" ) {
	$goalOther = "yes";
}
else {
	$goalOther = "no";
}

if ( @result[40] == 0 ) {
	$familiarityC = "None";
}
elsif ( @result[40] == 1 ) {
	$familiarityC = "Some";
}
elsif ( @result[40] == 2 ) {
	$familiarityC = "Intermediate";
}
elsif ( @result[40] == 3 ) {
	$familiarityC = "Expert";
}

if ( @result[41] == 0 ) {
        $familiarityJava = "None";
}
elsif ( @result[41] == 1 ) {
        $familiarityJava = "Some";
}
elsif ( @result[41] == 2 ) {
        $familiarityJava = "Intermediate";
}
elsif ( @result[41] == 3 ) {
        $familiarityJava = "Expert";
}

if ( @result[42] == 0 ) {
        $familiarityPython = "None";
}
elsif ( @result[42] == 1 ) {
        $familiarityPython = "Some";
}
elsif ( @result[42] == 2 ) {
        $familiarityPython = "Intermediate";
}
elsif ( @result[42] == 3 ) {
        $familiarityPython = "Expert";
}

if ( @result[43] == 0 ) {
        $familiarityMATLAB = "None";
}
elsif ( @result[43] == 1 ) {
        $familiarityMATLAB = "Some";
}
elsif ( @result[43] == 2 ) {
        $familiarityMATLAB = "Intermediate";
}
elsif ( @result[43] == 3 ) {
        $familiarityMATLAB = "Expert";
}

if ( @result[44] == 0 ) {
        $familiarityR = "None";
}
elsif ( @result[44] == 1 ) {
        $familiarityR = "Some";
}
elsif ( @result[44] == 2 ) {
        $familiarityR = "Intermediate";
}
elsif ( @result[44] == 3 ) {
        $familiarityR = "Expert";
}

if ( @result[63] eq "on" ) {
	$includingSecondReference = "yes";
}

if ( @result[79] == 0 ) {
	$uploadPersonalStatement_text = "will be typed in";
}
else {
	$uploadPersonalStatement_text = "will be uploaded";
}

if ( @result[81] == 0 ) {
	$mailLetterOfRec_text = "reference will send via e-mail";
}
else {
	$mailLetterOfRec_text = "reference will send via postal mail";
}

if ( @result[82] == 0 ) {
	$mailUnofficialTrans_text = "will be uploaded";
}
else {
	$mailUnofficialTrans_text = "will be sent via postal mail";
}

if ( @result[84] eq "on" ) {
	$fromProf = "yes";
}
else {
	$fromProf = "no";
}

if ( @result[85] eq "on" ) {
	$fromWeb = "yes";
}
else {
	$fromWeb = "no";
}

if ( @result[86] eq "on" ) {
	$fromPPart = "yes";
}
else {
	$fromPPart = "no";
}

if ( @result[87] eq "on" ) {
	$fromAd = "yes";
}
else {
	$fromAd = "no";
}

if ( @result[88] eq "on" ) {
	$fromOther = "yes";
}
else {
	$fromOther = "no";
}

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Registration number:</b> @result[0]</td><td><b>Submitted:</b> @result[1]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>First name:</b> @result[2] </td><td><b>Last name:</b> @result[3]</td><td><b>DOB:</b> @result[4]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>E-mail address:</b> @result[5]</td><td><b>Phone number:</b> @result[6]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Address:</b> @result[7]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>City:</b> @result[8]</td><td><b>State:</b> @result[9]</td><td><b>ZIP: </b>@result[10]</td><td><b>Country:</b> @result[11]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Is the above the permanent address:</b> $isPermanentAddress_text</td></tr>\n";
print "</table>\n";

# Only print permanent address information if it exists
if ( @result[12] == 0 ) {
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Permanent address:</b> @result[13]</td></tr>\n";
	print "</table>\n";
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>City:</b> @result[14]</td><td><b>State:</b> @result[15]</td><td><b>ZIP:</b> @result[16]</td><td><b>Country:</b> @result[17]</td></tr>\n";
	print "</table>\n";
}

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Is US Citizen or Permanent Resident:</b> $isUSCitizenOrPR_text</td><td><b>Ethnicity:</b> @result[19]</td><td><b>Gender:</b> $reportedGender_text</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Current University:</b> @result[21]</td><td><b>Academic level:</b> @result[22]</td><td><b>Expected grad date:</b> @result[23]</td><td><b>Overall college GPA:</b> @result[24]</td><td><b>Overall High School GPA:</b> @result[25]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Standardized test type: </b> @result[26]</td><td><b>Standardized test score: </b> @result[27]</td></tr>\n";
print "</table>\n";

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Participate to learn: </b> $participateToLearn</td><td><b>Participate for resume: </b> $participateForResume</td><td><b>Participate for money: </b> $participateForMoney</td><td><b>Participate for networking: </b> $participateForNetworking</td><td><b>Participate for other: </b> $participateForOther</td></tr>\n";
print "</table>\n";

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Participate other text: </b> @result[33]</td></tr>\n";
print "</table>\n";




print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Goal grad school: </b> $goalGrad</td><td><b>Goal industry job: </b> $goalIndustry</td><td><b>Goal lab job: </b> $goalLab</td><td><b>Goal other: </b> $goalOther</td></tr>\n";
print "</table>\n";

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Goal other text: </b> @result[38]</td></tr>\n";
print "</table>\n";

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Dream job: </b> @result[39]</td></tr>\n";
print "</table>\n";

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Familiarity C: </b> $familiarityC</td><td><b>Familiarity Java: </b> $familiarityJava</td><td><b>Familiarity Python: </b> $familiarityPython</td><td><b>Familiarity MATLAB: </b> $familiarityMATLAB</td><td><b>Familiarity R: </b> $familiarityR</td></tr>\n";
print "</table>\n";




print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Courses taken:</b> @result[45]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Awards or honors:</b> @result[46]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Genomics preference:</b> @result[47]</td><td><b>EHR preference:</b> @result[48]</td><td><b>Machine learning preference:</b> @result[49]</td><td><b>Data mining preference:</b> @result[50]</td></tr>\n";
print "</table>\n";
# 51 - reference first name
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one first name:</b> @result[51]</td><td><b>Reference one last name:</b> @result[52]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one title:</b> @result[53]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one relation to applicant:</b> @result[54]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one institution:</b> @result[55]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one address:</b> @result[56]</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one city:</b> @result[57]</td><td><b>Reference one state:</b> @result[58]</td><td><b>Reference one ZIP:</b> @result[59]</td><td><b>Reference one country:</b> @result[60]</td></tr>\n";
print "</table>\n";


print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Reference one phone:</b> @result[61]</td><td><b>Reference one e-mail:</b> @result[62]</td></tr>\n";
print "</table>\n";



print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Including second reference:</b> $includingSecondReference</td></tr>\n";
print "</table>\n";








# Only print second reference information if it was specified.
if (@result[63] eq "on") {
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two first name:</b> @result[64]</td><td><b>Reference two last name:</b> @result[65]</td></tr>\n";
	print "</table>\n";
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two title:</b> @result[66]</td></tr>\n";
	print "</table>\n";
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two relation to applicant:</b> @result[67]</td></tr>\n";
	print "</table>\n";
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two institution:</b> @result[68]</td></tr>\n";
	print "</table>\n";
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two address:</b> @result[69]</td></tr>\n";
	print "</table>\n";
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two city:</b> @result[70]</td><td><b>Reference two state:</b> @result[71]</td><td><b>Reference two ZIP:</b> @result[72]</td><td><b>Reference two country:</b> @result[73]</td></tr>\n";
	print "</table>\n";


	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Reference two phone:</b> @result[74]</td><td><b>Reference two e-mail:</b> @result[75]</td></tr>\n";
	print "</table>\n";
}

#print "<table cellspacing=0 cellpadding=10 border=0>\n";
#print "<tr><td><b>Personal statement source:</b> $uploadPersonalStatement_text</td></tr>\n";
#print "</table>\n";

if ( @result[76] == 1 ) {
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	$personalStatementURL_text = "<a href=\"@result[77]\">download</a>";
	print "<tr><td><b>Personal statement URL:</b> $personalStatementURL_text</td></tr>\n";
print "</table>\n";
}

#if ( @result[42] == 0 ) {
#	print "<table cellspacing=0 cellpadding=10 border=0>\n";
#	print "<tr><td><b>Personal statement:</b> @result[44]</td></tr>\n";
#	print "</table>\n";
#}

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Letter of recommendation source:</b> $mailLetterOfRec_text</td></tr>\n";
print "</table>\n";
print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Unofficial transcript source:</b> $mailUnofficialTrans_text</td></tr>\n";
print "</table>\n";

if ( $mailUnofficialTrans_text eq "will be uploaded") {
	print "<table cellspacing=0 cellpadding=10 border=0>\n";
	print "<tr><td><b>Unofficial transcript URL:</b> <a href=\"@result[83]\">download</a></td></tr>\n";
	print "</table>\n";
}

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>CV or resume URL:</b> <a href=\"@result[78]\">download</a></td></tr>\n";
print "</table>\n";






print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>From prof: </b> $fromProf</td><td><b>From Web: </b> $fromWeb</td><td><b>From past participant: </b> $fromPPart</td><td><b>From advertisment: </b> $fromAd</td><td><b>From other: </b> $fromOther</td></tr>\n";
print "</table>\n";

print "<table cellspacing=0 cellpadding=10 border=0>\n";
print "<tr><td><b>Find out about other text: </b> @result[89]</td></tr>\n";
print "</table>\n";








print "</td></tr>\n";

print <<END;
</table>
<p>
<center>
<form>
<input type="button" VALUE="Back" onClick="history.go(-1);return true;">
</form>
</center>
<p>
</body>
</html>
END

}

else {

# --- Print list of applicants ---

# Determine total number of rows
$query = "SELECT COUNT(*) FROM registrations";
$sth = $dbh->prepare($query);
$sth->execute;
$totalrows = $sth->fetchrow_array;

# determine order number
# this needs to be in ascending order otherwise we can't properly
# find the last previous order number.
$query = "SELECT * FROM registrations ORDER BY orderNumber ASC;";
$sth = $dbh->prepare($query);
$sth->execute;

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Transforming Analytical Learning in the Era of Big Data: Administrator</title>
</head>
<body>
<center>
<h2>Transforming Analytical Learning in the Era of Big Data - Attendee Roster</h2>
<p>
Total number of applicants is $totalrows. Select an applicant to jump to detail view.
<p>
<form action="/cgi-bin/admin/admin.cgi" method="POST">
<table cellspacing=0 cellpadding=10 border=0>
<tr><th>Registration number</th><th>First name</th><th>Last name</th><th>E-mail address</th><th>Select</th></tr>
END

$bar = 0;

do {
	@result = $sth->fetchrow_array;

	if ( scalar @result != 0 ) {

		# Do a little alternating color bar for each row to make it easier to read
		if ( $bar == 0 ) {
			$rowHeader = "<tr bgcolor=#dddddd>";
		}
		else {
			$rowHeader = "<tr>";
		}

		print $rowHeader . "<td>@result[0]</td><td>@result[2]</td><td>@result[3]</td><td>@result[5]</td><td><input type=\"radio\" name=\"selectedApplicant\" value=\"@result[0]\"></td></tr>\n";

		$bar = !$bar;

	}


} while (scalar @result != 0);

print <<END;
</table>
<p>
<input name="submit" type="submit" value="Select">
</form>
</center>
</body>
</html>
END
}

$dbh->disconnect();

# End of script

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

