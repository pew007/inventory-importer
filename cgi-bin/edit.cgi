#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use File::Basename;
use JSON;
use DBI;

####################################################################
### constants
$CGI::POST_MAX = 1024 * 3000; # Limit file size to 3MB
my $upload_dir = '/home/vagrant/public_html/proj1/_p_images';
my $safe_filename_chars = "a-zA-Z0-9_.-";
####################################################################

# my $host = "opatija.sdsu.edu";
# my $username = "jadrn048";
# my $password = "outlet";
my $host     = '127.0.0.1';
my $port     = "3306";
my $database = "jadrn048";
my $username = 'root';
my $password = "";
my $database_source = "dbi:mysql:$database:$host:$port";

my $cgi             = new CGI;
my $sku             = $cgi->param('sku');
my $category        = $cgi->param('category');
my $vendor          = $cgi->param('vendor');
my $platform        = $cgi->param('platform');
my $vendor_model    = $cgi->param('vendorModel');
my $description     = $cgi->param('description');
my $features        = $cgi->param('features');
my $cost            = $cgi->param('cost');
my $retail          = $cgi->param('retail');
my $filename        = $cgi->param("image");
my $new_filename    = get_new_filename($filename);

print $cgi->header;

if (validate_session()) {
    if ($filename ne undef) {
        upload_image();
    }
    update_product();
} else {
    get_json_response('SessionError', 'Invalid session.');
}

sub upload_image {

    unless($filename) {
        get_json_response('Error', 'Empty filename.');
    }

    my $mimetype = $cgi->uploadInfo($filename)->{'Content-Type'};

    # check the mime type and if it is not an image, reject it.
    if($mimetype !~ /image/) {
        die "Invalid mime type, $mimetype";
    }

    # get a handle on the uploaded image
    my $filehandle = $cgi->upload("image");

    unless($filehandle) { die "Invalid handle"; }

    # save the file
    open UPLOADFILE, ">$upload_dir/$new_filename" or die
        "Error, cannot save the file.";
    binmode UPLOADFILE;
    while(<$filehandle>) {
        if($_ =~ /\<\?php/) {
            die "Invalid file, php tag found!";
            }
        print UPLOADFILE $_;
        }
    close UPLOADFILE;
}

sub get_new_filename {
    my ($filename) = @_;

    my ($name, $path, $extension) = fileparse($filename, qr/\.[^.]*/);
    $filename = $sku.$extension;
    $filename =~ s/ //; #remove any spaces
    if($filename !~ /^([$safe_filename_chars]+)$/) {
        die "Sorry, invalid character in the filename.";
    }

    $filename = untaint($filename);
    $filename = lc($filename);

    return $filename;
}

sub untaint {
    if($filename =~ m/^(\w+)$/) { die "Tainted filename!"; }
    return $1;
}

sub update_product {

    my $dbh = DBI->connect($database_source, $username, $password)
    or die 'Cannot connect to db';

    my $statement = "
UPDATE product
SET categoryID = $category,
    vendorID = $vendor,
    platformID = $platform,
    vendorModel = '$vendor_model',
    description = '$description',
    features = '$features',
    cost = $cost,
    retail = $retail
WHERE sku = '$sku'";

    my $sth = $dbh->prepare($statement);
    $sth->execute();
    $sth->finish();
    $dbh->disconnect();

    my $vendorName   = find_by_id($vendor, 'vendor');
    my $categoryName = find_by_id($category, 'category');
    my $platformName = find_by_id($platform, 'platform');

    my $html = <<EOF;
<tr id="productRecord" data-sku=$sku role="row" class="even">
    <td class="sorting_1">$sku</td>
    <td>$vendorName</td>
    <td>$categoryName</td>
    <td>$platformName</td>
    <td>$vendor_model</td>
    <td>$cost</td>
    <td>$retail</td>
    <td><button class="edit">Edit</button></td>
    <td><button class="delete">Delete</button></td>
    <td class="hide">$description</td>
    <td class="hide">$features</td>
    <td class="hide">$new_filename</td>
</tr>
EOF

    get_json_response('OK', $html);
}

sub get_json_response {
    my ($status, $message) = @_;

    my %response_hash = ('status' => $status, 'message' => $message);
    my $json = encode_json \%response_hash;

    print $json;
}

sub find_by_id {
    my ($id, $table) = @_;
    my $itemId = '';
    my $itemName = '';

    if ($table eq 'vendor') {
        $itemId = 'vendorID';
        $itemName = 'vendorName';
    }

    if ($table eq 'category') {
        $itemId = 'categoryID';
        $itemName = 'categoryName';
    }

    if ($table eq 'platform') {
        $itemId = 'platformID';
        $itemName = 'platformName';
    }

    my $dbh = DBI->connect($database_source, $username, $password)
    or die 'Cannot connect to db';

    my $statement = "SELECT $itemName FROM $table WHERE $itemId = $id";
    my $sth = $dbh->prepare($statement);
    $sth->execute();
    my $result = $sth->fetch()->[0];

    $dbh->disconnect();

    return $result;
}

sub validate_session {
    my $cookie_sid = $cgi->cookie('jadrn048SID');
    my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});
    my $sid = $session->id;

    if($cookie_sid ne $sid) {
        return 0;
    } else {return 1;}
}
