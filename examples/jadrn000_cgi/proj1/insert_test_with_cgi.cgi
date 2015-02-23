#!/usr/bin/perl

use DBI;
use CGI;


print "content-type: text/html\n\n";
print "<html><body><h1>Perl to DB Test</h1></body>\n";
print "</html>\n";
my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "jadrn000";
my $username = "jadrn000";
my $password = "apple";
my $database_source = "dbi:mysql:$database:$host:$port";
my $response = "";

my $sku = 'ABC-123';
my $vendor = 2;
my $category = 1;
my $vendor_model = 'Ti6';
my $description = 'Entry level DSLR';
my $features = '20 MP';
my $cost = 649.50;
my $retail = 899.99;
my $image = 'ABC-123.jpg';

########################################################
### connect
my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

########################################################
### empty the products table
$dbh->do("DELETE FROM product");

########################################################
### insert a new product
my $statement = "INSERT INTO product values(".
"'$sku',$vendor,$category,'$vendor_model','$description',".
"'$features',$cost,$retail,'$image');";
print "The statement is \n$statement\n<br />";

$how_many = $dbh->do($statement);
print "$how_many rows affected\n<br />";

########################################################
### search for the product and display the data

#my $sth = $dbh->prepare("SELECT * FROM product");
$statement = "SELECT sku, category.name, vendor.name, vendorModel, retail ".
	" FROM vendor, category, product WHERE vendor.vendorID=product.venID and ".
	" category.categoryID=product.catID;";

print "\nThe statement is\n$statement\n<br />";
my $sth = $dbh->prepare($statement);
$sth->execute();

print "Data found in the database<br />\n";

while(my @rows = $sth->fetchrow_array()) {
    foreach $item (@rows) {
        print "$item  ";
        }
    print "\n"
    }

$sth->finish();
$dbh->disconnect();
