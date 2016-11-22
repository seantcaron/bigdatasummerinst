#!/usr/bin/perl

use DBI;
use DBD::mysql;
use Digest::MD5 qw(md5 md5_hex md5_base64);
# Requires: apt-get install cpanminus && cpanm -i Digest::SHA1
#use Digest::SHA1 qw(sha1 sha1_hex sha1_base64);
# Requires: apt-get install cpanminus && cpanm -i Digest::SHA
#use Digest::SHA qw(sha256_hex);

# Requires:  cpanm -i Crypt::Digest::SHA256
use Crypt::Digest::SHA256 qw(sha256 sha256_hex sha256_b64);

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

# Get form input passed from the WWW server.

if ($ENV{'REQUEST_METHOD'} eq "GET") {
        $input = $ENV{'QUERY_STRING'};
}

else {
        $input = <STDIN>;
}

# Initialize variables

$firstName = "";
$lastName = "";
$eMailAddress = "";
$confirmEMailAddress = "";
$phoneNumber = "";
$institutionalAffiliation = "";
$currentPosition = "";
$undergradMajor = "";
$undergradYear = "";
$attendingPDD = "";
$desiresTravelSuppt = "";
$presentingPoster = "";
$posterTitle = "";
$posterAbstract = "";

# Parse input

@inputs = split("&", $input);

foreach $pair (@inputs) {
        ($key, $value) = split("=", $pair);

        $value = sanitize($value);

        if ($key eq 'firstName') {
		$firstName = $value;
        }

        if ($key eq 'lastName') {
		$lastName = $value;
        }

	if ($key eq 'eMailAddress') {
		$eMailAddress = $value;
	}

	if ($key eq 'confirmEMailAddress') {
		$confirmEMailAddress = $value;
	}

	if ($key eq 'phoneNumber') {
		$phoneNumber = $value;
	}

	if ($key eq 'institutionalAffiliation') {
		$institutionalAffiliation = $value;
	}

	if ($key eq 'currentPosition') {
		$currentPosition = $value;
	}

	if ($key eq 'undergradMajor') {
		$undergradMajor = $value;
	}

	if ($key eq 'undergradYear') {
		$undergradYear = $value;
	}

	if ($key eq 'attendingPDD') {
		$attendingPDD = $value;
	}

	if ($key eq 'desiresTravelSuppt') {
		$desiresTravelSuppt = $value;
	}

	if ($key eq 'presentingPoster') {
		$presentingPoster = $value;
	}

	if ($key eq 'posterTitle') {
		$posterTitle = $value;
	}

	if ($key eq 'posterAbstract') {
		$posterAbstract = $value;
	}

}

open LOGFILE, ">/tmp/symp_int.log";
print LOGFILE $firstName . "\n";
print LOGFILE $lastName . "\n";
print LOGFILE $eMailAddress . "\n";
print LOGFILE $confirmEMailAddress . "\n";
print LOGFILE $phoneNumber . "\n";
print LOGFILE $institutionalAffiliation . "\n";
print LOGFILE $currentPosition . "\n";
print LOGFILE $undergradMajor . "\n";
print LOGFILE $undergradYear . "\n";
print LOGFILE $attendingPDD . "\n";
print LOGFILE $desiresTravelSuppt . "\n";

# validate input
#  - make sure no invalid characters
#    - handled by sanitize()
#  - make sure no fields are too long
#    - handled below

# Err 1 first name out of bounds or blank
if ( (length($firstName) < 1) || (length($firstName) > 254) ) {
	handleInputError(1);
}

# Err 2 last name out of bounds or blank
if ( (length($lastName) < 1) || (length($lastName) > 254) ) {
	handleInputError(2);
}

# Err 3 e-mail address out of bounds or blank
if ( (length($eMailAddress) < 1) || (length($eMailAddress) > 254) ) {
	handleInputError(3);
}

# Err 4 confirmation e-mail out of bounds or blank
if ( (length($confirmEMailAddress) < 1) || (length($confirmEMailAddress) > 254) ) {
	handleInputError(4);
}

# Err 5 e-mail address does not match confirmation e-mail address
if ( $eMailAddress ne $confirmEMailAddress ) {
	handleInputError(5);
}

# Err 6 phone number blank or out of bounds
if ( (length($phoneNumber) < 1) || (length($phoneNumber) > 254)) {
	handleInputError(6);
}

# Err 7 institution blank or out of bounds
if ( (length($institutionalAffiliation) < 1) || (length($institutionalAffiliation) > 254)) {
	handleInputError(7);
}

# Err 8 position not selected
if ( $currentPosition eq "" ) {
	handleInputError(8);
}

# Err 9 position = undergraduate AND major blank or out of bounds
if ( ($currentPosition eq "Undergraduate student") && ( (length($undergradMajor) < 1) || (length($undergradMajor > 254)) ) ) {
	handleInputError(9);
}

# Err 10 position = undergraduate AND year not selected
if ( ($currentPosition eq "Undergraduate student") && ($undergradYear eq "") ) {
	handleInputError(10);
}

# Error 11 position = undergraduate AND Prof. Dev. Day not specified
if ( ($currentPosition eq "Undergraduate student") && ($attendingPDD eq "") ) {
	handleInputError(11);
}


# Error 13 position != undergrad and major was specified
if ( ($currentPosition ne "Undergraduate student") && ($undergradMajor ne "")) {
	handleInputError(13);
}

# Error 14 position != undergrad and year was specified
if ( ($currentPosition ne "Undergraduate student") && ($undergradYear ne "") ) {
	handleInputError(14);
}

# Error 15 position != undergrad and Prof. Dev. Day was specified
if ( ($currentPosition ne "Undergraduate student") && ($attendingPDD ne "") ) {
	handleInputError(15);
}

# Error 17 position != undergrad and presentingPoster was specified
if ( ($currentPosition ne "Undergraduate student") && ($presentingPoster ne "") ) {
	handleInputError(17);
}

# Error 18 presentingPoster was specified but posterTitle blank or exceeds length limits
if ( ($presentingPoster eq "1") && ( (length($posterTitle) < 1) || (length($posterTitle) > 4096) ) ) {
	handleInputError(18);
}

# Error 19 presentingPoster was specified but posterAbstract blank or exceeds length limits
if ( ($presentingPoster eq "1") && ( (length($posterAbstract) < 1) || (length($posterAbstract) > 4096) ) ) {
	handleInputError(19);
}

# check to make sure no duplicate registrant
#  - test email address against all records in DB

$query = "SELECT * FROM registrations where eMailAddress = " . "\'" . $eMailAddress . "\';";
$sth = $dbh->prepare($query);
$sth->execute;

$result = eval { $sth->fetchrow_arrayref->[1] };

# If we get any results back at all, we know that the registration is a
# duplicate.

if ($result) {
	handleDuplicateRegistration();
}

# Ensure that we haven't hit the registrant limit (40 people).
# Make sure that we're only counting people who have actually paid, so a bunch of unpaid registrations won't
# run it up to the enrollment limit and prevent further (legit) people from registering.
$query = "SELECT COUNT(*) FROM registrations where totalCost != 0;";
$sth = $dbh->prepare($query);
$sth->execute;

$totalrows = $sth->fetchrow_array;

if ( $totalrows >= 65 ) {
	handleTooManyRegistrations();
}

# determine order number

# this needs to be in ascending order otherwise we can't properly
# find the last previous order number.
$query = "SELECT * FROM registrations ORDER BY orderNumber ASC;";
$sth = $dbh->prepare($query);
$sth->execute;

@result = $sth->fetchrow_array;

# If no records in table, start off with order number 3000 (to help further distinguish from SeqShop)

# Year 2016: Change the order number base to 3500.
if ( scalar @result == 0) {
	$orderNumber = 3500;
}

# otherwise order number = last order number + 1

else {

	# iterate over all rows until we find the last order number
	# then order number = last order number + 1

	do {
		$lastOrderNumber = @result[0];

		@result = $sth->fetchrow_array;

	} while (scalar @result != 0);

	$orderNumber = $lastOrderNumber + 1;

}

# Determine cost
# Undergraduate and graduate students $25
# Postdocs, faculty and other $50
if (($currentPosition eq "Undergraduate student") || ($currentPosition eq "Graduate student")) {
	$totalCost = 25;
}

else {
	$totalCost = 50;
}

# construct an insert command for the database

# patch up for non undergraduate applicants
if ($attendingPDD eq "") {
	$attendingPDD = 9;
}

if ($desiresTravelSuppt eq "") {
	$desiresTravelSuppt = 9;
}

if ($undergradMajor eq "") {
	$undergradMajor = "N/A";
}

if ($undergradYear eq "") {
	$undergradYear = "N/A";
}

if ($presentingPoster eq "") {
	$presentingPoster = 9;
}

if ($posterTitle eq "") {
	$posterTitle = "N/A";
}

if ($posterAbstract eq "") {
	$posterAbstract = "N/A";
}

$query = "INSERT INTO registrations VALUES ( " . $orderNumber . ", now(), " . "\'" . $firstName . "\', \'" . $lastName . "\', \'" . $eMailAddress . "\', \'" . $phoneNumber . "\', \'" . $institutionalAffiliation . "\', \'" . $currentPosition . "\', \'" . $undergradMajor . "\', \'" . $undergradYear . "\'," . $attendingPDD . "," . $desiresTravelSuppt . "," . $presentingPoster . ",\'" . $posterTitle . "\',\'" . $posterAbstract . "\'," . $totalCost . ",\'false\');";

print LOGFILE $query . "\n";
close LOGFILE;

# insert the record

$sth = $dbh->prepare($query);
$sth->execute;

# generate and show registration complete page + route to nelnet
#  - embed order number, cost in nelnet URL generated and inserted into
#    page.

# Time needs to be expressed in milliseconds for Nelnet.
$timeStamp = time * 1000;

# Set this to whatever the Nelnet people tell us to use.
$orderType="Michigan Genomics";

# Read in Nelnet password.
open NELNETKEYFILE, "</etc/apache2/nelnetkey.registrations";
# For testing: $keyString = "key";
# For production: $keyString = <NELNETKEYFILE>;
$keyString = <NELNETKEYFILE>;
close NELNETKEYFILE;
# For testing, comment out the line below.
chomp $keyString;

# Convert totalCost (aka amountDue) to cents for nelnet
$totalCost = $totalCost * 100;

# Nelnet documentation says orderType comes before orderNumber, but in the errata
# orderNumber comes prior to orderType and THIS IS WHAT MUST BE DONE FOR IT TO WORK.
# amountDue is totalCost
$tempHashInput = $orderNumber.$orderType.$totalCost.$timeStamp.$keyString;

# Be sure to use sha256_hex() and not md5() to calculate the hash.
$hashVal = sha256_hex($tempHashInput);

# Write out the interstitial page.

# For production: <form action="https://quikpayasp.com/umich2/commerce_manager/payer.do" METHOD="GET">
# For testing: <form action="https://uatquikpayasp.com/umich2/commerce_manager/payer.do" METHOD="GET">
print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Symposium Registration Pending Payment</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
The registration process is almost complete. Please click the button below to proceed to payment processing.
<p>
<font color=red><h3>Important! Please have your credit card ready in order to complete registration and payment.</h3></font>
<form action="https://quikpayasp.com/umich2/commerce_manager/payer.do" METHOD="GET">
<input name="orderType" type="hidden" value="$orderType" />
<input name="orderNumber" type="hidden" value="$orderNumber" />
<input name="amountDue" type="hidden" value="$totalCost" />
<input name="timestamp" type="hidden" value="$timeStamp" />
<input name="hash" type="hidden" value="$hashVal" />
<input name="Continue" type="submit" value="Continue" /></p>
</form>
</center>
</body>
</html>
END

# Send confirmation e-mail to the end user so they will know that they have been entered into the
# registration database.

$smtp = Net::SMTP->new("localhost");

$smtp->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp->recipient($eMailAddress);

$smtp->data();
$smtp->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu\n");
$smtp->datasend("To: " . $eMailAddress . "\n");
$smtp->datasend("Subject: University of Michigan Summer Institute in Biostatistics Symposium Registration Confirmation\n");
$smtp->datasend("\n");
$smtp->datasend("Thank you for your interest in the University of Michigan, Department of Biostatistics, School of Public Health Big Data Summer Institute Symposium, July 21-22, 2016.\n\n");
$smtp->datasend("All events on July 21 will take place in the Rackham Building fourth floor and the undergraduate professional development workshop will take place in the School of Public Health, SPH II auditorium.\n\n");
$smtp->datasend("You have been added to our list of attendees and a confirmation e-mail will be sent to your contact e-mail address.\n\n\n");
$smtp->datasend("Registration is finalized once your payment information has been received. If you were not able to enter your credit card information upon registering, please contact Irene Felicetti at ilf\@umich.edu.\n\n");
$smtp->datasend("Please note that the registration fee will appear on your credit card statement as Michigan Genomics.\n\n");
$smtp->datasend("We look forward to seeing you on July 21.\n");

$smtp->dataend();
$smtp->quit;

# Send a brief message to Irene so someone knows that a new registration has
# come in.
$smtp = Net::SMTP->new("localhost");

$smtp->mail("do-not-reply\@bigdatasummerinst.sph.umich.edu");
$smtp->recipient("ilf\@umich.edu");

$smtp->data();
$smtp->datasend("From: do-not-reply\@bigdatasummerinst.sph.umich.edu\n");
$smtp->datasend("To: ilf\@umich.edu\n");
$smtp->datasend("Subject: U-M Summer Institute in Biostatistics Symposium New Registration\n");
$smtp->datasend("\n");
$smtp->datasend("A new registration for the SIBS Symposium has been entered into the system. Please check payment status when time permits.\n\n");

$smtp->dataend();
$smtp->quit;

# Remember to disconnect from the database.
$dbh->disconnect();

sub handleTooManyRegistrations {

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Attendee Limit Reached</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Registration for the symposium is full. Please contact Irene Felicetti at ilf@umich.edu for further assistance.
<p>
<form><input type="button" VALUE="Back" onCLick="history.go(-1);return true;"></form>
</center>
</body>
</html>
END

exit;
}

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
Someone has already applied for the symposium with the e-mail address specified. Please confirm your registration information and try again.
<p>
<form><input type="button" VALUE="Back" onCick="location.href=document.referrer; return true;"></form>
</center>
</body>
</html>
END

exit;
}

sub handleInputError {

	$errorCode = @_[0];

	if ( $errorCode == 1 ) {
		$errorText = "the first name field was left blank or exceeded length limits";
	}

	elsif ( $errorCode == 2 ) {
		$errorText = "the last name field was left blank or exceeded length limits";
	}

        elsif ( $errorCode == 3 ) {
		$errorText = "the e-mail field was left blank or exceeded length limits";
        }

	elsif ( $errorCode == 4) {
		$errorText = "the e-mail confirmation field was left blank or exceeded length limits";
	}

	elsif ( $errorCode == 5) {
		$errorText = "the e-mail address did not match the confirmation e-mail address";
	}

	elsif ( $errorCode == 6) {
		$errorText = "the phone number field was left blank or exceeded length limits";
	}

	elsif ( $errorCode == 7) {
		$errorText = "the institutional affiliation field was left blank or exceeded length limits";
	}

	elsif ( $errorCode == 8) {
		$errorText = "no current position was selected";
	}

	elsif ( $errorCode == 9) {
		$errorText = "undergraduate student status was selected, and major field was left blank or exceeded length limits";
	}

	elsif ( $errorCode == 10) {
		$errorText = "undergraduate student status was selected, and no year was selected";
	}

	elsif ( $errorCode == 11) {
		$errorText = "undergraduate student status was selected, and professional development day attendance was not specified";
	}

	elsif ( $errorCode == 12) {
		$errorText = "undergraduate student status was selected, and travel support interest was not specified";
	}

	elsif ( $errorCode == 13) {
		$errorText = "undergraduate student status was not selected, and a major was specified";
	}

	elsif ( $errorCode == 14) {
		$errorText = "undergraduate student status was not selected, and an academic year was specified";
	}

	elsif ( $errorCode == 15) {
		$errorText = "undergraduate student status was not selected, and professional development day attendance was specified";
	}

	elsif ( $errorCode == 16) {
		$errorText = "undergraduate student status was not selected, and travel support interest was specified";
	}

	elsif ( $errorCode == 17) {
		$errorText = "undergraduate student status was not selected, and a poster presentation choice was specified";
	}

	elsif ( $errorCode == 18) {
		$errorText = "poster presentation was specified but the title field was left blank or exceeded length limits";
	}

	elsif ( $errorCode == 19) {
		$errorText = "poster presentation was specified but the abstract field was left blank or exceeded length limits";
	}

	else {
		$errorText = "of an undefined error";
	}

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Symposium Registration Error</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Your registration could not be processed because $errorText.
<p>
Please confirm your registration information and try again.
<p>
<form><input type="button" VALUE="Back" onCLick="location.href=document.referrer;return true;"></form>
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

