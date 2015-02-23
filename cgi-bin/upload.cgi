#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
use File::Basename;
use JSON;

####################################################################
### constants
$CGI::POST_MAX = 1024 * 3000; # Limit file size to 3MB
my $upload_dir = '/home/vagrant/public_html/proj1/_p_images';
my $safe_filename_chars = "a-zA-Z0-9_.-";
####################################################################

my $cgi = new CGI;
upload_image();
get_json_response();

sub upload_image {
    my $filename = $cgi->param("image");
    unless($filename) {
        die "There was a problem uploading the image; ".
            "it's probably too big.";
    }

    my $mimetype = $cgi->uploadInfo($filename)->{'Content-Type'};

    # check the mime type and if it is not an image, reject it.
    if($mimetype !~ /image/) {
        die "Invalid mime type, $mimetype";
    }

    # Use SKU as new filename
    $filename = get_new_filename($filename);

    # get a handle on the uploaded image
    my $filehandle = $cgi->upload("image");

    unless($filehandle) { die "Invalid handle"; }

    # save the file
    open UPLOADFILE, ">$upload_dir/$filename" or die
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

    my $sku = $cgi->param('sku');
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

sub get_json_response {
    my $sku             = $cgi->param('sku');
    my $category        = $cgi->param('category');
    my $vendor          = $cgi->param('vendor');
    my $platform        = $cgi->param('platform');
    my $vendor_model    = $cgi->param('vendorModel');
    my $description     = $cgi->param('description');
    my $features        = $cgi->param('features');
    my $cost            = $cgi->param('cost');
    my $retail          = $cgi->param('retail');

    my $json->{"status"} = $sku;
    my $json_text = to_json($json);

    print $cgi->header('application/json');

    print $json_text;
}
