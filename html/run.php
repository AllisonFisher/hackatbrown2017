<?php

function _get($name) {
  if (isset($_GET[$name]))
    return $_GET[$name];
  return null;
}

function run_python($script) {
  ob_start();
  passthru("/usr/bin/python3 $script 2>&1 > output.txt");
  return ob_get_clean();
}


$fps = "1/10";
$yt_url = _get('url');

if ($yt_url != null) {
  echo "<pre>";
  echo run_python("analyzer/start.py --input $yt_url --fps $fps");
  echo "</pre>";
} else {
  echo "Nah.";
}

?>

