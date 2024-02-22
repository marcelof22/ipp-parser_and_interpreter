<?php

/**
 * @author Feiler Marcel
 * @file parse.php
 * @date 10.03.2023
 * @project Parser of PHP code family
 */

 ini_set('display_errors', 'stderr');

 define("HEADER_REGEX", "/^\.(?i)ippcode23$/");
 define("INTEGER_REGEX", "/^int\@{1}([+-]?\d+((?i)[e][-]?\d+)?|0(?i)[o][0-7]+|0(?i)[x][0-9a-fA-F]+)$/");
 define("BOOLEAN_REGEX", "/^bool\@{1}(true|false){1}$/");
 define("NIL_REGEX", "/^nil\@{1}nil$/");
 define("TYPE_REGEX", "/^(int|nil|bool|string)\@{1}/");
 define("DATATYPE_REGEX", "/^(int|bool|string)$/");
 define("VARIABLE_REGEX", "/^(GF|TF|LF){1}\@{1}[a-zA-Z\_\-\$\&\%\*\!\?]{1}[a-zA-Z0-9\_\-\$\&\%\*\!\?]*$/");
 define("LABEL_REGEX", "/^[a-zA-Z\_\-\$\&\%\*\!\?][a-zA-Z0-9\_\-\$\&\%\*\!\?]*$/");
 define("STRING_REGEX", "/^string\@{1}[^\s]*[\w\-\$\&\%\*\!\?\>\<\/áčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]*$/");
 define("STRING_FORBIDDEN_REGEX", "/\\\\\d{0,2}(?!\d)/");
 

 //global $argv, $argc;
 $shortOpts = "h";
 $longOpts = array(
    "help"
 );
 $getOpts = getopt($shortOpts, $longOpts);

 //--help, -h params checking
 if (array_key_exists("help", $getOpts) || array_key_exists("h", $getOpts)) {
    if ($argc == 2 && ($argv[1] == "-h" || $argv[1] == "--help")) {
        echo "Help statements:\n";
        echo "-h, --help   =>  Showing help information.\n";
        exit(0);
   
    }
    else {
        exit(10); // returns 10 if anything additional excepting -h OR --help
    }
 }

 syntax();
 exit(0);


 function create_xml($xml) {
    //creating of xml writer

    //vytvorenie xml writera
    $xml = new \XMLWriter();
    //inicializacia xml suboru
    $xml->openMemory();
    //odsadenie elementov
    $xml->setIndent(TRUE);
    //pocet medzier odsadenia elementov
    $xml->setIndentString(' ');
    //startDocument je vytvorenie XML hlavicky - parametre : verzia 1.0 a znak. sada UTF-8
    $xml->startDocument('1.0', 'UTF-8');
    //vytvorenie elementu s nazvom program
    $xml->startElement('program');
    //vpisanie atributu language s hodnotou IPPcode23
    $xml->writeAttribute('language', 'IPPcode23');

    return $xml;
 }
 /*** */
 function is_header($line) {
    return preg_match(HEADER_REGEX, $line);
 }
 /*** */
 function end_xml($xml) {
    $xml->endElement();
    $xml->endDocument();
    fwrite(STDOUT, $xml->flush());
 }
 /*** */
 function hard_exit_xml($xml, $error) {
    
    
    //$xml->endElement();
    //$xml->endDocument();
    //unset($xml);
    exit($error);
 }
 /*** */
 function remove_blank_comments($line) {  
        //to remove comments and unify white spaces
       

        $line = preg_replace("/\#.*/", "", $line);
        $line = preg_replace("/^\s*$/", "", $line); // from BEG to END white spaces

        $line = preg_replace("/[\r\n\v]/", "", $line);
        $line = preg_replace("/^\s*/", "", $line);  //removing before instruction
        $line = preg_replace("/\s*$/", "", $line);
        $line = preg_replace("/\s+/", " ", $line);
        return $line; //return clear  
 }

 /*** */
 function empty_line($line) {
    return preg_match("/^\s*$/", $line);
 }
 /*** */
 /*** */


 /*** */
 function operands_check($operands, $xml, $instruction) {
    $pocet = count($operands);
    //echo "{$pocet}";

    switch(count($operands)) {
        case 0:
            switch(strtoupper($instruction)) {
                case "CREATEFRAME":
                case "PUSHFRAME":
                case "POPFRAME":
                case "RETURN":
                case "BREAK":
                    return;

                default: hard_exit_xml($xml, 23);
            }
            
            
        case 1:
            switch(strtoupper($instruction)) {
                // 1 variable instruction
                case "DEFVAR": #DEFVAR
                case "POPS": #POPS
                    //echo "tusom\n";
                    if (!preg_match(VARIABLE_REGEX, $operands[0])) {
                        //echo "defvar cek\n";
                        hard_exit_xml($xml, 23);
                    }
                    //echo"tusom\n";
                    return;
                
            
            
                //operand with one constant or one var
                case "PUSHS":     # PUSHS
                case "WRITE":    # WRITE
                case "EXIT":    # EXIT
                case "DPRINT":    # DPRINT
                    if (!preg_match(VARIABLE_REGEX, $operands[0]) && !preg_match(INTEGER_REGEX, $operands[0]) && !preg_match(STRING_REGEX, $operands[0]) && !preg_match(BOOLEAN_REGEX, $operands[0]) && !preg_match(NIL_REGEX, $operands[0])) {
                        hard_exit_xml($xml, 23);
                    }
                    return;
            
                // operand with only 1 label
                case "CALL": #CALL
                case "LABEL":    #LABEL
                case "JUMP":    #JUMP
                    if(!preg_match(LABEL_REGEX, $operands[0])) {
                        hard_exit_xml($xml, 23);
                    }
                    return;
                default: hard_exit_xml($xml, 23);

            }



        case 2:
            switch(strtoupper($instruction)) {
                // operand with : 1 var 1 constant 
                case "MOVE":    #MOVE
                case "NOT":    #NOT
                case "INT2CHAR":    #INT2CHAR
                case "STRLEN":    #STRLEN
                case "TYPE":    #TYPE
                    if(preg_match(VARIABLE_REGEX, $operands[0])) {
                        

                        if (!preg_match(VARIABLE_REGEX, $operands[1]) && !preg_match(INTEGER_REGEX, $operands[1]) && !preg_match(STRING_REGEX, $operands[1]) && !preg_match(BOOLEAN_REGEX, $operands[1]) && !preg_match(NIL_REGEX, $operands[1])) {
                            hard_exit_xml($xml, 23);
                        }
                        
                    }

                    else {
                        hard_exit_xml($xml, 23);
                    }
                    return; //pay attention

                //one var one type operand
                case "READ":    #READ
                    if(preg_match(VARIABLE_REGEX, $operands[0])) {
                        
                        if(!preg_match(DATATYPE_REGEX, $operands[1])) {
                            hard_exit_xml($xml, 23);
                        }

                    }

                    else {
                        hard_exit_xml($xml, 23);
                    }
                    return; //pay attention

                default: hard_exit_xml($xml, 23);
            }
        case 3:
            switch(strtoupper($instruction)) {
                case "ADD": #ADD
                case "SUB": #SUB
                case "MUL": #MUL
                case "IDIV": #IDIV
                case "LT": #LT
                case "GT": #GT
                case "EQ": #EQ
                case "AND": #AND
                case "OR": #OR
                case "STRI2INT": #STRI2INT
                case "CONCAT": #CONCAT
                case "GETCHAR": #GETCHAR
                case "SETCHAR": #SETCHAR
                    if(preg_match(VARIABLE_REGEX, $operands[0])) {

                        if (!preg_match(VARIABLE_REGEX, $operands[1]) && !preg_match(INTEGER_REGEX, $operands[1]) && !preg_match(STRING_REGEX, $operands[1]) && !preg_match(BOOLEAN_REGEX, $operands[1]) && !preg_match(NIL_REGEX, $operands[1])) {
                            hard_exit_xml($xml, 23);
                        }

                        if (!preg_match(VARIABLE_REGEX, $operands[2]) && !preg_match(INTEGER_REGEX, $operands[2]) && !preg_match(STRING_REGEX, $operands[2]) && !preg_match(BOOLEAN_REGEX, $operands[2]) && !preg_match(NIL_REGEX, $operands[2])) {
                            hard_exit_xml($xml, 23);
                        }
                        
                    }

                    else {
                        hard_exit_xml($xml, 23);
                    }
                    return; //pay attention
            
            

                case "JUMPIFEQ": #JUMPIFEQ
                case "JUMPIFNEQ": #JUMPIFNEQ
                    if(preg_match(LABEL_REGEX, $operands[0])) {

                        if (!preg_match(VARIABLE_REGEX, $operands[1]) && !preg_match(INTEGER_REGEX, $operands[1]) && !preg_match(STRING_REGEX, $operands[1]) && !preg_match(BOOLEAN_REGEX, $operands[1]) && !preg_match(NIL_REGEX, $operands[1])) {
                            hard_exit_xml($xml, 23);
                        }

                        if (!preg_match(VARIABLE_REGEX, $operands[2]) && !preg_match(INTEGER_REGEX, $operands[2]) && !preg_match(STRING_REGEX, $operands[2]) && !preg_match(BOOLEAN_REGEX, $operands[2]) && !preg_match(NIL_REGEX, $operands[2])) {
                            hard_exit_xml($xml, 23);
                        }
                        
                    }

                    else {
                        hard_exit_xml($xml, 23);
                    }
                    return; //pay attention

                default: hard_exit_xml($xml, 23);
            }
        
        
        
    }
    
    
    //echo "ahoj\n";

}


 /*** */

 function instruction_check($line, $xml) {

    $instructions = array(
        "MOVE" => 2,
        "CREATEFRAME" =>0, // <var> <symb>
        "PUSHFRAME" =>0,   //
        "POPFRAME" =>0,    //
        "DEFVAR" =>1,      //
        "CALL" =>1,        //
        "RETURN" =>0,
        "PUSHS" =>1,
        "POPS" =>1,
        "ADD" =>3,
        "SUB" =>3,
        "MUL" =>3,
        "IDIV" =>3,
        "LT" =>3,
        "GT" =>3,
        "EQ" =>3,
        "AND" =>3,
        "OR" =>3,
        "NOT" =>2,
        "INT2CHAR" =>2,
        "STRI2INT" =>3,
        "READ" =>2,
        "WRITE" =>1,
        "CONCAT" =>3,
        "STRLEN" =>2,
        "GETCHAR" =>3,
        "SETCHAR" =>3,
        "TYPE" =>2,
        "LABEL" =>1,
        "JUMP" =>1,
        "JUMPIFEQ" =>3,
        "JUMPIFNEQ" =>3,
        "EXIT" =>1,
        "DPRINT" =>1,
        "BREAK" =>0);

    $temp = array();
    $temp = preg_split("/ /", $line);


    if (!empty($temp)) {
        $instruction = $temp[0];

        if (!array_key_exists(strtoupper($instruction), $instructions)) {
            
            hard_exit_xml($xml, 22); //instruction does not exist
        }

        if (!operand_count_check($instructions, $instruction, count($temp)-1)) {
            //here i go
            hard_exit_xml($xml, 23);
        }

        if (count($temp) > 1) { //only when instruction doesn't have any operands
            
            $operands = $temp;
            array_shift($operands); 
            //echo "imhere\n";
            operands_check($operands, $xml, $instruction);
            //echo"here please\n";
        }
        
        
    }

    return $temp;

    //check instruction without parametres
 }


 function operand_count_check($instructions, $instruction, $count) {
    return $instructions[$instruction] == $count;
 }



 function add_xml_instructions($checked_one, $xml, $instruction_counter) {
    $xml->startElement('instruction');
    $xml->writeAttribute('order', $instruction_counter);
    $xml->writeAttribute('opcode', strtoupper($checked_one[0])); //name of instruction

    if (count($checked_one) > 1) {
        for ($index = 1; $index < count($checked_one); $index++) {
            $xml->startElement('arg' . $index);

            //whether label, variable, constant

            if (preg_match(VARIABLE_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'var');
                $xml->text($checked_one[$index]);
                $xml->endElement();
            }

            else if (preg_match(INTEGER_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'int');
                $xml->text(preg_split("/\@/", $checked_one[$index])[1]);
                $xml->endElement();
            }

            else if (preg_match(BOOLEAN_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'bool');
                $xml->text(preg_split("/\@/", $checked_one[$index])[1]);
                $xml->endElement();
            }

            else if (preg_match(STRING_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'string');
                $xml->text(preg_split("/\@/", $checked_one[$index])[1]);
                $xml->endElement();
            }

            else if (preg_match(NIL_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'nil');
                $xml->text(preg_split("/\@/", $checked_one[$index])[1]);
                $xml->endElement();
            }

            else if (preg_match(LABEL_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'label');
                $xml->text($checked_one[$index]);
                $xml->endElement();
            }

            else if (preg_match(TYPE_REGEX, $checked_one[$index])) {
                $xml->writeAttribute('type', 'type');
                $xml->text($checked_one[$index]);
                $xml->endElement();
            }
            
            else {
                hard_exit_xml($xml, 23);
            }

        }

    }

    $xml->endElement();
 }


 function syntax() {
    $header = false;
    $xml = NULL;
    $instruction_counter = 0;
    
    while(!feof(STDIN)) {
        $line = fgets(STDIN);
        //echo "{$line}";
        //to remove blank spaces
        $line = remove_blank_comments($line);
       

        if ($header) {

            if(is_header($line)) {
                hard_exit_xml($xml, 22); //double header
            }
          
            if(!feof(STDIN) && !empty_line($line)) {
                
                $checked_one = instruction_check($line, $xml);
                //echo "dobree\n";
                $instruction_counter += 1;
                add_xml_instructions($checked_one, $xml, $instruction_counter);
            }
        }

        else {
           
            //finding header
            if (is_header($line)) {
                $header = true;
                $xml = create_xml($xml);
                
            }

            if (!$header && (!empty_line($line) || feof(STDIN))) {
                exit (21);  //missing header
            }
        }

        


    }

    if (isset($xml)) {
        end_xml($xml);
    }

 


 }

 syntax();
 exit(0);

