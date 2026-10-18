package main

import (
 "context"
 "encoding/json"
 "flag"
 "fmt"
 "log"
 "os"
 "path/filepath"
 "sort"
 "time"
 "github.com/xssnick/tonutils-go/address"
 "github.com/xssnick/tonutils-go/liteclient"
 "github.com/xssnick/tonutils-go/ton"
)
type Record struct { Pool string `json:"pool"`; LT uint64 `json:"lt"`; Detail string `json:"detail"` }
type Status struct {Pool string `json:"pool"`; Count int `json:"count"`; Complete bool `json:"complete"`; Error string `json:"error,omitempty"`}
func main(){
 output:=flag.String("out","../../artifacts/efhc-ton","output directory")
 flag.Parse()
 if err:=os.MkdirAll(*output,0755);err!=nil{log.Fatal(err)}
 pools:=map[string]string{
 "USDT_EFHC":"EQB2iz4-oG50xuXjbRYc-h-TR-Siow7ynH0XGNsor_lgg8D2",
 "GRAM_EFHC":"EQDMCqRzSnMtKjltr6jf4Fqah1o14Gdyq6sU5-XsNGkuIY9F",
 "RBTC_EFHC":"EQAlrp2dgYMHbtp1X0_KujyZvpTHkjjEvic4kBa1FlNRZa8s",
 }
 client:=liteclient.NewConnectionPool()
 ctx,cancel:=context.WithTimeout(context.Background(),15*time.Minute);defer cancel()
 if err:=client.AddConnectionsFromConfigUrl(ctx,"https://ton-blockchain.github.io/global.config.json");err!=nil{log.Fatal(err)}
 api:=ton.NewAPIClient(client,ton.ProofCheckPolicyFast).WithRetryTimeout(3,5*time.Second).WithLSInfoInErrors()
 block,err:=api.CurrentMasterchainInfo(ctx);if err!=nil{log.Fatal(err)}
 statuses:=[]Status{}
 for _,name:=range []string{"USDT_EFHC","GRAM_EFHC","RBTC_EFHC"}{
  s:=Status{Pool:name}; addr:=address.MustParseAddr(pools[name])
  f,err:=os.Create(filepath.Join(*output,name+".jsonl"));if err!=nil{log.Fatal(err)}
  enc:=json.NewEncoder(f)
  account,err:=api.GetAccount(ctx,block,addr)
  if err!=nil{s.Error=err.Error()}else{
   lt,hash:=account.LastTxLT,account.LastTxHash
   seen:=map[uint64]bool{}
   for lt!=0 {
    page,e:=api.ListTransactions(ctx,addr,15,lt,hash)
    if e!=nil{s.Error=e.Error();break}
    if len(page)==0{s.Error="empty page before genesis";break}
    sort.Slice(page,func(i,j int)bool{return page[i].LT>page[j].LT})
    oldest:=page[len(page)-1]
    if seen[oldest.LT]{s.Error="pagination stalled";break}
    for _,tx:=range page{
     if seen[tx.LT]{continue}
     seen[tx.LT]=true
     if e=enc.Encode(Record{Pool:name,LT:tx.LT,Detail:tx.String()});e!=nil{s.Error=e.Error();break}
     s.Count++
    }
    if s.Error!=""{break}
    lt,hash=oldest.PrevTxLT,oldest.PrevTxHash
   }
   if lt==0&&s.Error==""{s.Complete=true}
  }
  f.Close();statuses=append(statuses,s)
  fmt.Printf("%s: %d transactions, complete=%v, error=%s\n",name,s.Count,s.Complete,s.Error)
 }
 f,err:=os.Create(filepath.Join(*output,"status.json"));if err!=nil{log.Fatal(err)}
 if err=json.NewEncoder(f).Encode(statuses);err!=nil{log.Fatal(err)}
 f.Close()
 for _,s:=range statuses{if !s.Complete{os.Exit(2)}}
}
