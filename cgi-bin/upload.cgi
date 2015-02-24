#!/usr/bin/perl

use CGI;
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
my $host = '127.0.0.1';
my $port = "3306";
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

# Use SKU as new filename
my $new_filename    = get_new_filename($filename);

upload_image();
check_for_dup_sku();
insert_new_product();

sub upload_image {

    unless($filename) {
        die "There was a problem uploading the image; ".
            "it's probably too big.";
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

sub check_for_dup_sku {
    # body...
}

sub insert_new_product {

    my $dbh = DBI->connect($database_source, $username, $password)
    or die 'Cannot connect to db';

    my $statement = "INSERT INTO product values(" .
        "'$sku', $category, $vendor, $platform, '$vendor_model', '$description', '$features', $cost, $retail, '$new_filename');";

    my $rows = $dbh->do($statement);
    $dbh->disconnect();

    if ($rows > 0) {
        get_json_response('OK');
    } else {
        get_json_response('Error');
    }
}

sub get_json_response {

    my ($status) = @_;

    my $json->{"status"} = $status;
    my $json_text = to_json($json);

    print $cgi->header('application/json');

    print $json_text;
}
