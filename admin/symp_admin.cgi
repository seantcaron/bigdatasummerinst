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

$paidCount = 0;

@inputs = split("&", $input);

foreach $pair (@inputs) {
        ($key, $value) = split("=", $pair);

        $value = sanitize($value);
	$key = sanitize($key);

	if ( $value eq 'on' ) {
		($paid, $orderNumber) = split(":", $key);

		@paidRegistrants[$paidCount] = $orderNumber;

		$paidCount = $paidCount + 1;
	}

}

# Mark any as paid that were marked as such by the end user in the previous run.

$updateCount = 0;

while ( $updateCount < $paidCount ) {
	$query = "UPDATE registrations SET hasPaid = 'true' where orderNumber = " . @paidRegistrants[$updateCount] . ";";

	$sth = $dbh->prepare($query);
	$sth->execute;

	$updateCount = $updateCount + 1;
}

# determine total number of rows.

$query = "SELECT COUNT(*) FROM registrations";
$sth = $dbh->prepare($query);
$sth->execute;

$totalrows = $sth->fetchrow_array;

# determine total number of paid registrations

$query = "SELECT COUNT(*) FROM registrations where hasPaid = 'true'";
$sth = $dbh->prepare($query);
$sth->execute;

$totalpaid = $sth->fetchrow_array;

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
<title>Transforming Analytical Learning in the Era of Big Data Symposium - Attendee Roster</title>
</head>
<body>
<center>
<h2>Transforming Analytical Learning in the Era of Big Data Symposium - Attendee Roster</h2>
<p>
Total number of attendees is $totalrows
<br>
Total number of paid attendees is $totalpaid
<p>
<form action="/cgi-bin/admin/symp_admin.cgi" method="POST">
<table cellspacing=0 cellpadding=10 border=0>
<tr><th>markAsPaid</th><th>orderNumber</th><th>registrationTime</th><th>firstName</th><th>lastName</th><th>eMailAddress</th><th>phoneNumber</th><th>institutionalAffiliation</th><th>currentPosition</th><th>undergradMajor</th><th>undergradYear</th><th>attendingPDD</th><th>desiresTravelSuppt</th><th>presentingPoster</th><th>posterTitle</th><th>posterAbstract</th><th>totalCost</th><th>hasPaid</th></tr>
END

$bar = 0;

do {
	@result = $sth->fetchrow_array;

	if ( scalar @result != 0 ) {

		if ( @result[10] == 0 ) {
			$attendingPDD = "false";
		}

		elsif ( @result[10] == 9 ) {
			$attendingPDD = "N/A";
		}

		else {
			$attendingPDD = "true";
		}

		if ( @result[11] == 0 ) {
			$desiresTravelSuppt = "false";
		}

		elsif ( @result[10] == 9 ) {
			$desiresTravelSuppt = "N/A";
		}

		else {
			$desiresTravelSuppt = "true";
		}

		if ( @result[12] == 0 ) {
			$presentingPoster = "false";
		}

		elsif ( @result[12] == 9 ) {
			$presentingPoster = "N/A";
		}

		else {
			$presentingPoster = "true";
		}

		if ( $bar == 0 ) {
			print "<tr bgcolor=#dddddd><td align=center><input type=\"checkbox\" name=\"paid:@result[0]\"></td><td>@result[0]</td><td>@result[1]</td><td>@result[2]</td><td>@result[3]</td><td>@result[4]</td><td>@result[5]</td><td>@result[6]</td><td>@result[7]</td><td>@result[8]</td><td>@result[9]</td><td>$attendingPDD</td><td>$desiresTravelSuppt</td><td>$presentingPoster</td><td>@result[13]</td><td>@result[14]</td><td>@result[15]</td><td>@result[16]</td></tr>\n";
		}

		else {
			print "<tr><td align=center><input type=\"checkbox\" name=\"paid:@result[0]\"></td><td>@result[0]</td><td>@result[1]</td><td>@result[2]</td><td>@result[3]</td><td>@result[4]</td><td>@result[5]</td><td>@result[6]</td><td>@result[7]</td><td>@result[8]</td><td>@result[9]</td><td>$attendingPDD</td><td>$desiresTravelSuppt</td><td>$presentingPoster</td><td>@result[13]</td><td>@result[14]</td><td>@result[15]</td><td>@result[16]</td></tr>\n";
		}

	$bar = !$bar;

	}


} while (scalar @result != 0);

print <<END;
</table>
<p>
<input name="Submit" type="submit" value="Update Marked Registrants">
</form>
</center>
</body>
</html>
END

$dbh->disconnect();

# End

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

