import {useState} from "react";
export default function App(){
  const [url,setUrl]=useState("");
  const [msg,setMsg]=useState("");
  const importUrl=async()=>{
    const r=await fetch("http://127.0.0.1:8000/import",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url})});
    setMsg(JSON.stringify(await r.json()));
  };
  return (<div style={{fontFamily:"sans-serif",padding:24,maxWidth:800}}>
    <h1>AudioScope v0.1</h1>
    <input value={url} onChange={e=>setUrl(e.target.value)} placeholder="URL YouTube" style={{width:"100%",padding:8}}/>
    <button onClick={importUrl} style={{marginTop:8,padding:"8px 16px"}}>Importer</button>
    <p>{msg}</p>
    <video controls style={{width:"100%",marginTop:16}} src=""/>
  </div>);
}
