#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
use JSON;

my $cgi = new CGI;

my $sku             = $cgi->param('sku');
my $category        = $cgi->param('category');
my $vendor          = $cgi->param('vendor');
my $platform        = $cgi->param('platform');
my $vendor_model    = $cgi->param('vendorModel');
my $description     = $cgi->param('description');
my $features        = $cgi->param('features');
my $cost            = $cgi->param('cost');
my $retail          = $cgi->param('retail');
my $image           = $cgi->param('image');

my $json->{"status"} = 'OK';
my $json_text = to_json($json);

print $cgi->header('application/json');

print $json_text;


