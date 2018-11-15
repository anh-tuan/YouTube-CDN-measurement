<html>
<hed>
<title>Replace HTML Code</title>
<meta charset="UTF-8">
</head>
<body style="font-family: Arial;">
<p align="center" style="font-size: 20pt;">URL Parser</p>
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
	
	$getparams = explode("?", $input);

	$params = explode("&", $getparams[1]);

	sort($params);

	$result = "";
	foreach ($params as &$param) {
		$result = $result . $param . "\n";
	}
	//count($params)

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
