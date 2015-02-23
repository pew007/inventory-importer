#!/usr/bin/perl 
#	Sample perl cgi script.  This script prints a list of the 
#	KEY=VALUE parameters received from the client.
#	CS545 Fall 2011
#	Code by Alan Riggins
#
use CGI;

my $q = new CGI;

print <<END_HTML;
Content-type: text/html

<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
	<title>CGI Script that echoes parameters</title>
	<meta http-equiv="content-type" 
		content="text/html;charset=utf-8" />
	<meta http-equiv="Content-Style-Type" content="text/css" />

    
<style type="text/css">
body { background-color: #CCCCEE; }
table { 
	margin-left: auto; margin-right: auto; 
	}
h1, h2 { text-align: center; }
td {	
	text-align: center; 
	background-color: white; 
	border: 2px solid black; 
	width: 400px; 
	}
</style>
</head>
<body><div>
<h1>Example Form and CGI Script</h1>
<h2>You have submitted the following 
<i><b>key=value</b></i> parameter pairs</h2>
<br /><br />
<table>
END_HTML
		
my ($key, $value);
                
foreach $key ($q->param) {
    print "<tr>\n";
    print "<td>$key</td>\n";
    foreach $value ($q->param($key)) {
        print "<td>$value</td>\n";
        }
    print "</tr>\n";
}
print "</table>\n";
print "</div>\n";
print "</body>\n";
print "</html>\n";

