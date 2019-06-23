#!/usr/bin/perl

use strict;
use warnings;

my $filename = "lanl-auth-dataset-1";
my $start = 1;
my $interval = 900;
my $end = $start + $interval;
my $bucket = 0;
open(my $file, $filename) or die("Failed to open input file");
while(my $row = <$file>) {
	#print("Row: $row");
	chomp($row);
	my @tokens = split(/,/, $row);
	my $timestamp = $tokens[0] + 0;
	#print("Is $timestamp greater than $end?");
	if($timestamp > $end) {
		print("$bucket,\n");
		$bucket = 0;
		$start = $end;
		$end += $interval;
	}
	else {
		$bucket++;
	}
}