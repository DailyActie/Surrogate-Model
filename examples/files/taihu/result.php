<?php
    // header('Content-Type: application/json');

    //echo '--php:Start::['.(new \DateTime())->format('Y-m-d H:i:s')."] result.php\n";
    $taihudir = '/var/www/html/taihu';
    $resultdir = 'result';
    $casename = '';

    $varname = 'GREENS';
    $iseg  = -9999;
    $itime = -9999;

    $output = '';
    $rtnJSON = array(
        "his" => "",
        "map" => "",
        "json"=> "",
        "py" => "",
    );

    if( $_GET['c'] && $_GET['v'] ) {
    // && $_GET['s'] && $_GET['t']
        // $casename = sprintf('%s%08d', $_GET['pref'], intval($_GET['c']));
        $casename = sprintf($resultdir.'/%s%08d', $_GET['pref'], intval($_GET['c']));
        $varname  = $_GET['v'];

        if( $_GET['p'] >= 0 ){
            $iseg  = intval($_GET['p']);
        }
        if( $_GET['p'] == -9999 ){
            $iseg  = intval($_GET['p']);
        }

        if( $_GET['t'] >= 0){
            $itime = intval($_GET['t']);
        }
        if( $_GET['t'] == -9999){
            $itime = intval($_GET['t']);
        }

        if( $casename && $varname ) {
            $exe_py_cmd = 'python /var/www/html/taihu/d3d_read_map.py'
                           .' -d '.$taihudir
                           .' -c '.$casename
                           .' -v '.$varname
                           .' -p '.$iseg
                           .' -t '.$itime
                           .' 2>&1';
            exec($exe_py_cmd,$output,$returnval);
            $rtnJSON['py']  = $output;
            // foreach( $output as $text ){ echo "$text\n"; }
            //
            $rtnJSON['his']   = $casename.'/his_'.$varname.'_s'.$iseg.'.png?'.(new \DateTime())->format('YmdHis');
            $rtnJSON['map']   = $casename.'/map_'.$varname.'_t'.$itime.'.png?'.(new \DateTime())->format('YmdHis');
            $rtnJSON['json']  = $casename.'/map_'.$varname.'_t'.$itime.'.json?'.(new \DateTime())->format('YmdHis');
            echo json_encode($rtnJSON);
        }

    } else {
        echo '--php:Error:: check input!\n';
        print_r($_GET);
    }
    //echo '--php:End:: ['.(new \DateTime())->format('Y-m-d H:i:s')."]\n";
?>

