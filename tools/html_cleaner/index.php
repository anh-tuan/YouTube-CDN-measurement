<html>
<hed>
<title>Replace HTML Code</title>
<meta charset="UTF-8">
</head>
<body style="font-family: Arial;">
<p align="center" style="font-size: 20pt;">Replace HTML code</p>
<form action="./" method="POST" name="form">
<p align="center">
Input:<br />
<textarea rows="20" cols="120" name="input">
<?php 
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	echo $_REQUEST['input']; 
}
?>
</textarea>
<br /><br /><input type="submit">
</p>
</form>

<p></p>

<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
	$input = $_REQUEST['input'];
	
	$result = str_replace("%20", " ", $input);
	$result = str_replace("%21", "!", $result);
	$result = str_replace('%22', '"', $result);
	$result = str_replace("%23", "#", $result);
	$result = str_replace("%24", "$", $result);
	$result = str_replace("%25", "%", $result);
	$result = str_replace("%26", "&", $result);
	$result = str_replace("%27", "'", $result);
	$result = str_replace("%28", "(", $result);
	$result = str_replace("%28", ")", $result);
	$result = str_replace("%2A", "*", $result);
	$result = str_replace("%2B", "+", $result);
	$result = str_replace("%2C", ",", $result);
	$result = str_replace("%2D", "-", $result);
	$result = str_replace("%2E", ".", $result);
	$result = str_replace("%2F", "/", $result);
	$result = str_replace("%3A", ":", $result);
	$result = str_replace("%3B", ";", $result);
	$result = str_replace("%3D", "=", $result);
	$result = str_replace("%3F", "?", $result);
	$result = str_replace("%40", "@", $result);
	$result = str_replace("%5B", "[", $result);
	$result = str_replace("%5D", "]", $result);
	$result = str_replace("%5F", "_", $result);
	$result = str_replace("%96", "-", $result);
	$result = str_replace("%A6", "|", $result);
	$result = str_replace("\u0026", "&", $result);	

?>
	<p align="center">
	Output:<br />
	<textarea rows="20" cols="120" name="output"><?php echo $result; ?></textarea>
</p>

<?php  
}
?>

</body>
</html>
