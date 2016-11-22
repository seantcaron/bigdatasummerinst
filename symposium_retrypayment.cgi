#!/usr/bin/perl

use DBI;
use DBD::mysql;
use Digest::MD5 qw(md5 md5_hex md5_base64);
# Requires: apt-get install cpanminus && cpanm -i Digest::SHA1
use Digest::SHA1 qw(sha1 sha1_hex sha1_base64);
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

$eMailAddress = "";

# Parse input

@inputs = split("&", $input);

foreach $pair (@inputs) {
        ($key, $value) = split("=", $pair);

        $value = sanitize($value);

	if ($key eq 'eMailAddress') {
		$eMailAddress = $value;
	}
}

# validate input
#  - make sure no invalid characters
#    - handled by sanitize()
#  - make sure no fields are too long
#    - handled below

if ( (length($eMailAddress) < 1) || (length($eMailAddress) > 254) ) {
	handleInputError();
}

# locate the registrant in the database by e-mail address. if we don't get any results back,
# there must not already be a registration with that e-mail, so bounce them back with an
# error message.

$query = "SELECT * FROM registrations WHERE eMailAddress = \'" . $eMailAddress . "\';";
$sth = $dbh->prepare($query);
$sth->execute;

@result = $sth->fetchrow_array;

# if no records returned, no registration by that e-mail address
if ( scalar @result == 0) {
	handleUnregisteredAttendee();
}

# otherwise collect all the pertinent information about the attendee needed to construct the
# nelnet link again.
else {

	$orderNumber = @result[0];

	$hasPaid = @result[13];

	$currentPosition = @result[7];
}

if ( $hasPaid eq 'true' ) {
	handleAlreadyPaid();
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

# generate and show registration complete page + route to nelnet
#  - embed order number, cost in nelnet URL generated and inserted into
#    page.

# Time needs to be expressed in milliseconds for Nelnet.
$timeStamp = time * 1000;

# Set this to whatever the Nelnet people tell us to use.
$orderType="Michigan Genomics";

# Read in Nelnet password.
open NELNETKEYFILE, "</etc/apache2/nelnetkey.registrations";
$keyString = <NELNETKEYFILE>;
close NELNETKEYFILE;
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
print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Continue To Payment</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Please click the button below to proceed to payment processing.
<p>
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

# Remember to disconnect from the database.
$dbh->disconnect();

sub handleUnregisteredAttendee {

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Registration Not Found</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
No registrant was found in the database with the e-mail address supplied. Please confirm your e-mail address and try again.
<p>
<form><input type="button" VALUE="Back" onCLick="history.go(-1);return true;"></form>
</center>
</body>
</html>
END

exit;

}

sub handleInputError {

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Invalid E-Mail Address</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
Your request could not be processed because the e-mail address field was left blank or exceeded length limits.
<p>
Please confirm your e-mail address and try again.
<p>
<form><input type="button" VALUE="Back" onCLick="history.go(-1);return true;"></form>
</center>
</body>
</html>
END

exit;

}

sub handleAlreadyPaid {

print <<END;
Content-Type: text/html\n\n
<html>
<head>
<title>Registrant Already Paid</title>
</head>
<body>
<center>
<img src="http://bigdatasummerinst.sph.umich.edu/templates/beez_20/images/personal/personal2.png" align=bottom alt="[header]">
<p>
The attendee registered with the e-mail address submitted is already marked as having paid.
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

