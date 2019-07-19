<?php
$numberOfAppointments = 6;
$customAppointmentsFile = getcwd() .'/appointments.csv';
$appointmentTemplateFile = getcwd() .'/appointment.tpl';

$k4cgArr = Array();
$labArr = Array();

$year = date('Y');
$month = date('m');

$customAppointmentsK4cgArr = Array();
$customAppointmentsLabArr = Array();

$row = 1;
if(file_exists($customAppointmentsFile)) {
  if (($handle = fopen($customAppointmentsFile, 'r')) !== FALSE) {
    while (($data = fgetcsv($handle, 1000, ',')) !== FALSE) {
      $row++;

      if($row>1) { //ignore header line
        switch($data[0]) {
          case 'k4cg':
            $customAppointmentsK4cgArr[$data[1]] = $data[2];
            break;
          case 'lab':
            $customAppointmentsLabArr[$data[1]] = $data[2];
            break;
          default:
            break;
        }
      }
    }
    fclose($handle);
  } else {
    echo "error";
  }
} else {
  echo 'file not found';
}

while(count($k4cgArr)<$numberOfAppointments && count($labArr)<$numberOfAppointments) {
  $yearMonth = "$year-$month";

  if(count($k4cgArr)<$numberOfAppointments) {
  $k4cgAppointment = strtotime("first thursday of $yearMonth");

    if($k4cgAppointment>strtotime('today')) {
      if(array_key_exists($yearMonth, $customAppointmentsK4cgArr)) {
        $k4cgArr[] = $customAppointmentsK4cgArr[$yearMonth];
      } else {
        $k4cgArr[] = date('d.m.Y', $k4cgAppointment);
      }
    }
  }

  if(count($labArr)<$numberOfAppointments) {
    $labAppointment = strtotime("third tuesday of $yearMonth");

    if($k4cgAppointment>strtotime('today')) {
      if(array_key_exists($yearMonth, $customAppointmentsLabArr)) {
        $labArr[] = $customAppointmentsLabArr[$yearMonth];
      } else {
        $labArr[] = date('d.m.Y', $labAppointment);
      }
    }
  }

  $year = date('Y', strtotime('+1 month', strtotime($yearMonth)));
  $month = date('m', strtotime('+1 month', strtotime($yearMonth)));
}

$k4cgArr = array_reverse($k4cgArr);
$labArr = array_reverse($labArr);

$template = file_get_contents($appointmentTemplateFile);
    
$output = '';
for($i=0;$i<$numberOfAppointments;$i++) {
  $tmp = $template;
  $tmp = str_replace('{{date}}', array_pop($k4cgArr), $tmp);
  $tmp = str_replace('{{location}}', 'K4CG', $tmp);
  $output .= $tmp;

  $tmp = $template;
  $tmp = str_replace('{{date}}', array_pop($labArr), $tmp);
  $tmp = str_replace('{{location}}', 'Fablab Region Nürnberg', $tmp);
  $output .= $tmp;
}
echo $output;

?>  

