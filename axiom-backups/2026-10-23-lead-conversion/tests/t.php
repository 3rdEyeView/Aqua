<?php
namespace { define('ABSPATH','/');
$POSTS=[10=>['feedback','publish',1096,time()-30],11=>['feedback','spam',1096,time()-30],12=>['feedback','publish',999,time()-30],13=>['feedback','publish',1096,time()-3600],14=>['page','publish',1096,time()]];
function get_post($id){global $POSTS; if(!isset($POSTS[$id]))return null; $p=new stdClass; [$p->post_type,$p->post_status,$p->post_parent,$p->t]=$POSTS[$id]; return $p;}
function get_post_time($f,$g,$p){return $p->t;}
function add_filter(){} function add_action(){}
function wp_json_encode($v){return json_encode($v);} function esc_url_raw($u){return $u;} function rest_url($p){return 'https://x/wp-json/'.$p;}
$src=file_get_contents(__DIR__.'/../snippet-1099-main.after.php');
$src=str_replace("const LEAD_CONVERSION_SEND_TO = '';","const LEAD_CONVERSION_SEND_TO = 'AW-TEST/label';",$src);
file_put_contents(__DIR__.'/t-snip.php',$src); require __DIR__.'/t-snip.php';
foreach([10=>'accepted',11=>'spam',12=>'other form',13=>'too old',14=>'not feedback',99=>'missing'] as $id=>$n) echo str_pad($n,13).' countable='.var_export(\AngieSnippets\AxiomGetStartedForm_1099\lead_is_countable($id),true)."\n";
file_put_contents(__DIR__.'/t-script.html',\AngieSnippets\AxiomGetStartedForm_1099\lead_tracking_script());
}
