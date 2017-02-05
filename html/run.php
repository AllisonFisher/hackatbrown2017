<?php

function _post($name) {
  if (isset($_POST[$name]))
    return $_POST[$name];
  return null;
}

function _get($name) {
  if (isset($_GET[$name]))
    return $_GET[$name];
  return null;
}

$fps = "1/10";
$yt_url = _post('url');

if ($yt_url != null) {
  echo shell_exec("cd /home/ethan/hackatbrown2017/youtube; python start.py --input $yt_url --fps $fps");
} else {
  echo "Nah.";
}

?>

