<?php
# encrypt/decrypt string (assumes blank secret, null salt)

define('PATH_LIBRARY', '/var/www/openphoto/src/libraries');
include PATH_LIBRARY . '/models/Utility.php';

if (count($argv)!=3) die("usage: $argv[0] <encrypt|decrypt> string\n");

$action = $argv[1];
$string = $argv[2];
$utility = new Utility();

switch ($action) {
    case "encrypt":
        print $utility->encrypt($string, "", null);
        break;
    case "decrypt":
        print $utility->decrypt($string, "", null);
        break;
    default:
        die("supported actions: encrypt, decrypt");
        break;
}

?>

