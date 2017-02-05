<?php

header("Refresh:1");

if (isset($_GET['file'])) {
  $file = $_GET['file'];
  echo "<pre>";
  echo file_get_contents($file);
  echo "</pre>"; 
}

?>
