import{P as Ge,Q as ze,J as _e,D as Je,s as le,r as ce,i as I,n as ie,f as m,e as g,t as B,c as b,b as S,d as R,h as c,j as W,a as y,m as fe,g as O,R as be,S as Z,o as d,G as Ve,T as Te,U as x,V as He,B as De,W as Ke,l as Ye,u as We,p as Xe,q as Ze,X as Se,Y as Me,w as xe}from"../chunks/scheduler.xWvB5Pfl.js";import{g as ke,a as z,c as ve,t as M,S as ne,i as oe,b as ee,d as te,m as se,e as re}from"../chunks/index.BNVms-Pv.js";function et(l,e){const t=e.token={};function s(r,n,u,o){if(e.token!==t)return;e.resolved=o;let i=e.ctx;u!==void 0&&(i=i.slice(),i[u]=o);const f=r&&(e.current=r)(i);let h=!1;e.block&&(e.blocks?e.blocks.forEach((a,_)=>{_!==n&&a&&(ke(),z(a,1,1,()=>{e.blocks[_]===a&&(e.blocks[_]=null)}),ve())}):e.block.d(1),f.c(),M(f,1),f.m(e.mount(),e.anchor),h=!0),e.block=f,e.blocks&&(e.blocks[n]=f),h&&Je()}if(Ge(l)){const r=ze();if(l.then(n=>{_e(r),s(e.then,1,e.value,n),_e(null)},n=>{if(_e(r),s(e.catch,2,e.error,n),_e(null),!e.hasCatch)throw n}),e.current!==e.pending)return s(e.pending,0),!0}else{if(e.current!==e.then)return s(e.then,1,e.value,l),!0;e.resolved=l}}function tt(l,e,t){const s=e.slice(),{resolved:r}=l;l.current===l.then&&(s[l.value]=r),l.current===l.catch&&(s[l.error]=r),l.block.p(s,t)}function he(l){return(l==null?void 0:l.length)!==void 0?l:Array.from(l)}function Ce(l){let e,t;return{c(){e=g("mark"),t=B(l[0])},l(s){e=b(s,"MARK",{});var r=S(e);t=R(r,l[0]),r.forEach(m)},m(s,r){I(s,e,r),c(e,t)},p(s,r){r&1&&W(t,s[0])},d(s){s&&m(e)}}}function st(l){let e,t=l[0]&&Ce(l);return{c(){t&&t.c(),e=ce()},l(s){t&&t.l(s),e=ce()},m(s,r){t&&t.m(s,r),I(s,e,r)},p(s,[r]){s[0]?t?t.p(s,r):(t=Ce(s),t.c(),t.m(e.parentNode,e)):t&&(t.d(1),t=null)},i:ie,o:ie,d(s){s&&m(e),t&&t.d(s)}}}function rt(l,e,t){let{message:s=""}=e;return l.$$set=r=>{"message"in r&&t(0,s=r.message)},[s]}class we extends ne{constructor(e){super(),oe(this,e,rt,st,le,{message:0})}}function qe(l,e,t){const s=l.slice();return s[1]=e[t],s[3]=t,s}function Pe(l){let e,t,s="Answer",r,n,u,o,i,f=l[0].text+"",h,a,_=he(l[0].documents),v=[];for(let p=0;p<_.length;p+=1)v[p]=ye(qe(l,_,p));return{c(){e=g("article"),t=g("h4"),t.textContent=s,r=y(),n=g("hr"),u=y(),o=g("blockquote"),i=g("cite"),h=B(f),a=y();for(let p=0;p<v.length;p+=1)v[p].c()},l(p){e=b(p,"ARTICLE",{});var w=S(e);t=b(w,"H4",{"data-svelte-h":!0}),fe(t)!=="svelte-1n2dwgk"&&(t.textContent=s),r=O(w),n=b(w,"HR",{}),u=O(w),o=b(w,"BLOCKQUOTE",{});var k=S(o);i=b(k,"CITE",{});var N=S(i);h=R(N,f),N.forEach(m),k.forEach(m),a=O(w);for(let q=0;q<v.length;q+=1)v[q].l(w);w.forEach(m)},m(p,w){I(p,e,w),c(e,t),c(e,r),c(e,n),c(e,u),c(e,o),c(o,i),c(i,h),c(e,a);for(let k=0;k<v.length;k+=1)v[k]&&v[k].m(e,null)},p(p,w){if(w&1&&f!==(f=p[0].text+"")&&W(h,f),w&1){_=he(p[0].documents);let k;for(k=0;k<_.length;k+=1){const N=qe(p,_,k);v[k]?v[k].p(N,w):(v[k]=ye(N),v[k].c(),v[k].m(e,null))}for(;k<v.length;k+=1)v[k].d(1);v.length=_.length}},d(p){p&&m(e),be(v,p)}}}function ye(l){let e,t,s="Source "+String(l[3]+1)+" : "+l[1].position,r,n,u,o=l[1].content+"",i,f;return{c(){e=g("details"),t=g("summary"),r=B(s),n=y(),u=g("blockquote"),i=B(o),f=y()},l(h){e=b(h,"DETAILS",{});var a=S(e);t=b(a,"SUMMARY",{});var _=S(t);r=R(_,s),_.forEach(m),n=O(a),u=b(a,"BLOCKQUOTE",{});var v=S(u);i=R(v,o),v.forEach(m),f=O(a),a.forEach(m)},m(h,a){I(h,e,a),c(e,t),c(t,r),c(e,n),c(e,u),c(u,i),c(e,f)},p(h,a){a&1&&s!==(s="Source "+String(h[3]+1)+" : "+h[1].position)&&W(r,s),a&1&&o!==(o=h[1].content+"")&&W(i,o)},d(h){h&&m(e)}}}function lt(l){let e,t=l[0].status=="ok"&&Pe(l);return{c(){t&&t.c(),e=ce()},l(s){t&&t.l(s),e=ce()},m(s,r){t&&t.m(s,r),I(s,e,r)},p(s,[r]){s[0].status=="ok"?t?t.p(s,r):(t=Pe(s),t.c(),t.m(e.parentNode,e)):t&&(t.d(1),t=null)},i:ie,o:ie,d(s){s&&m(e),t&&t.d(s)}}}function nt(l,e,t){let{answer:s}=e;return l.$$set=r=>{"answer"in r&&t(0,s=r.answer)},[s]}class ot extends ne{constructor(e){super(),oe(this,e,nt,lt,le,{answer:0})}}function Oe(l,e,t){const s=l.slice();return s[6]=e[t],s}function Ie(l){let e,t,s,r="Ask Questions",n,u,o,i,f,h,a,_,v="Select a book",p,w,k,N,q,$,L,j,G,E,K=l[1].answer.status=="processing"?"Processing":"Ask Question",T,A,U,P,X,J,Y,me,Ee,ae=he(l[0]),Q=[];for(let C=0;C<ae.length;C+=1)Q[C]=Ne(Oe(l,ae,C));return P=new we({props:{message:l[1].answer.error}}),J=new ot({props:{answer:l[1].answer}}),{c(){e=g("section"),t=g("article"),s=g("h4"),s.textContent=r,n=y(),u=g("hr"),o=y(),i=g("form"),f=g("label"),h=B(`Book
                    `),a=g("select"),_=g("option"),_.textContent=v;for(let C=0;C<Q.length;C+=1)Q[C].c();p=y(),w=g("label"),k=B(`Percentage
                    `),N=g("input"),q=y(),$=g("label"),L=B(`Question
                `),j=g("input"),G=y(),E=g("button"),T=B(K),U=y(),ee(P.$$.fragment),X=y(),ee(J.$$.fragment),this.h()},l(C){e=b(C,"SECTION",{id:!0});var F=S(e);t=b(F,"ARTICLE",{});var H=S(t);s=b(H,"H4",{"data-svelte-h":!0}),fe(s)!=="svelte-1stl1xm"&&(s.textContent=r),n=O(H),u=b(H,"HR",{}),o=O(H),i=b(H,"FORM",{});var V=S(i);f=b(V,"LABEL",{for:!0});var D=S(f);h=R(D,`Book
                    `),a=b(D,"SELECT",{name:!0,"aria-label":!0});var ue=S(a);_=b(ue,"OPTION",{"data-svelte-h":!0}),fe(_)!=="svelte-1jbl809"&&(_.textContent=v);for(let ge=0;ge<Q.length;ge+=1)Q[ge].l(ue);ue.forEach(m),D.forEach(m),p=O(V),w=b(V,"LABEL",{for:!0});var pe=S(w);k=R(pe,`Percentage
                    `),N=b(pe,"INPUT",{type:!0,name:!0,placeholder:!0,"aria-label":!0,min:!0,max:!0}),pe.forEach(m),q=O(V),$=b(V,"LABEL",{for:!0});var de=S($);L=R(de,`Question
                `),j=b(de,"INPUT",{type:!0,name:!0,placeholder:!0,"aria-label":!0}),de.forEach(m),G=O(V),E=b(V,"BUTTON",{"aria-busy":!0,class:!0});var $e=S(E);T=R($e,K),$e.forEach(m),V.forEach(m),U=O(H),te(P.$$.fragment,H),H.forEach(m),X=O(F),te(J.$$.fragment,F),F.forEach(m),this.h()},h(){_.selected=!0,_.disabled=!0,_.__value="",Z(_,_.__value),d(a,"name","book"),d(a,"aria-label","Select"),a.required=!0,l[1].book===void 0&&Ve(()=>l[3].call(a)),d(f,"for","book"),d(N,"type","number"),d(N,"name","percentage"),d(N,"placeholder","Percentage"),d(N,"aria-label","Percentage"),d(N,"min","0"),d(N,"max","100"),d(w,"for","percentage"),d(j,"type","search"),d(j,"name","question"),d(j,"placeholder","Your Question"),d(j,"aria-label","Search"),d($,"for","question"),d(E,"aria-busy",A=l[1].answer.status=="processing"),d(E,"class","full-width svelte-1p1u34"),d(e,"id","questions-form")},m(C,F){I(C,e,F),c(e,t),c(t,s),c(t,n),c(t,u),c(t,o),c(t,i),c(i,f),c(f,h),c(f,a),c(a,_);for(let H=0;H<Q.length;H+=1)Q[H]&&Q[H].m(a,null);Te(a,l[1].book,!0),c(i,p),c(i,w),c(w,k),c(w,N),Z(N,l[1].percentage),c(i,q),c(i,$),c($,L),c($,j),Z(j,l[1].question),c(i,G),c(i,E),c(E,T),c(t,U),se(P,t,null),c(e,X),se(J,e,null),Y=!0,me||(Ee=[x(a,"change",l[3]),x(N,"input",l[4]),x(j,"input",l[5]),x(E,"click",l[2])],me=!0)},p(C,F){if(F&1){ae=he(C[0]);let D;for(D=0;D<ae.length;D+=1){const ue=Oe(C,ae,D);Q[D]?Q[D].p(ue,F):(Q[D]=Ne(ue),Q[D].c(),Q[D].m(a,null))}for(;D<Q.length;D+=1)Q[D].d(1);Q.length=ae.length}F&3&&Te(a,C[1].book),F&3&&He(N.value)!==C[1].percentage&&Z(N,C[1].percentage),F&3&&j.value!==C[1].question&&Z(j,C[1].question),(!Y||F&2)&&K!==(K=C[1].answer.status=="processing"?"Processing":"Ask Question")&&W(T,K),(!Y||F&3&&A!==(A=C[1].answer.status=="processing"))&&d(E,"aria-busy",A);const H={};F&2&&(H.message=C[1].answer.error),P.$set(H);const V={};F&2&&(V.answer=C[1].answer),J.$set(V)},i(C){Y||(M(P.$$.fragment,C),M(J.$$.fragment,C),Y=!0)},o(C){z(P.$$.fragment,C),z(J.$$.fragment,C),Y=!1},d(C){C&&m(e),be(Q,C),re(P),re(J),me=!1,De(Ee)}}}function Ne(l){let e,t=l[6]+"",s,r,n;return{c(){e=g("option"),s=B(t),r=y(),this.h()},l(u){e=b(u,"OPTION",{});var o=S(e);s=R(o,t),r=O(o),o.forEach(m),this.h()},h(){e.__value=n=l[6],Z(e,e.__value)},m(u,o){I(u,e,o),c(e,s),c(e,r)},p(u,o){o&1&&t!==(t=u[6]+"")&&W(s,t),o&1&&n!==(n=u[6])&&(e.__value=n,Z(e,e.__value))},d(u){u&&m(e)}}}function at(l){let e,t,s=l[0].length>0&&Ie(l);return{c(){s&&s.c(),e=ce()},l(r){s&&s.l(r),e=ce()},m(r,n){s&&s.m(r,n),I(r,e,n),t=!0},p(r,[n]){r[0].length>0?s?(s.p(r,n),n&1&&M(s,1)):(s=Ie(r),s.c(),M(s,1),s.m(e.parentNode,e)):s&&(ke(),z(s,1,1,()=>{s=null}),ve())},i(r){t||(M(s),t=!0)},o(r){z(s),t=!1},d(r){r&&m(e),s&&s.d(r)}}}function ut(l,e,t){let{books:s=[]}=e,r={question:"",book:"",percentage:100,answer:{text:"",documents:[],status:"idle",error:""}};async function n(){try{t(1,r.answer={text:"",documents:[],status:"processing",error:""},r);const f=await fetch("ask-question",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(r)}),h=await f.json();f.ok?(t(1,r.answer.text=h.answer,r),t(1,r.answer.documents=h.documents,r),t(1,r.answer.status="ok",r)):(t(1,r.answer.error=h?JSON.stringify(h):f.statusText,r),t(1,r.answer.status="error",r))}catch(f){t(1,r.answer.status="error",r),t(1,r.answer.error=String(f),r)}}function u(){r.book=Ke(this),t(1,r),t(0,s)}function o(){r.percentage=He(this.value),t(1,r),t(0,s)}function i(){r.question=this.value,t(1,r),t(0,s)}return l.$$set=f=>{"books"in f&&t(0,s=f.books)},[s,r,n,u,o,i]}class ct extends ne{constructor(e){super(),oe(this,e,ut,at,le,{books:0})}}function Be(l){let e,t,s;return{c(){e=g("img"),this.h()},l(r){e=b(r,"IMG",{class:!0,src:!0,alt:!0}),this.h()},h(){d(e,"class","full-width svelte-zdk8qr"),Se(e.src,t=l[0].formats["image/jpeg"])||d(e,"src",t),d(e,"alt",s=l[0].title)},m(r,n){I(r,e,n)},p(r,n){n&1&&!Se(e.src,t=r[0].formats["image/jpeg"])&&d(e,"src",t),n&1&&s!==(s=r[0].title)&&d(e,"alt",s)},d(r){r&&m(e)}}}function Re(l){let e,t=l[0].authors.map(Le).reduce(Ue)+"",s;return{c(){e=g("p"),s=B(t),this.h()},l(r){e=b(r,"P",{class:!0});var n=S(e);s=R(n,t),n.forEach(m),this.h()},h(){d(e,"class","text svelte-zdk8qr")},m(r,n){I(r,e,n),c(e,s)},p(r,n){n&1&&t!==(t=r[0].authors.map(Le).reduce(Ue)+"")&&W(s,t)},d(r){r&&m(e)}}}function Ae(l){let e,t,s=l[0].languages.reduce(je)+"",r;return{c(){e=g("p"),t=B("Language : "),r=B(s)},l(n){e=b(n,"P",{});var u=S(e);t=R(u,"Language : "),r=R(u,s),u.forEach(m)},m(n,u){I(n,e,u),c(e,t),c(e,r)},p(n,u){u&1&&s!==(s=n[0].languages.reduce(je)+"")&&W(r,s)},d(n){n&&m(e)}}}function it(l){let e,t,s,r,n,u,o=l[0].title+"",i,f,h,a,_,v,p=l[0].formats["image/jpeg"]&&Be(l),w=l[0].authors.length>0&&Re(l),k=l[0].languages.length>0&&Ae(l);const N=l[2].default,q=Ye(N,l,l[1],null);return{c(){e=g("article"),t=g("figure"),p&&p.c(),s=y(),r=g("div"),n=g("hgroup"),u=g("h5"),i=B(o),f=y(),w&&w.c(),h=y(),k&&k.c(),a=y(),_=g("div"),q&&q.c(),this.h()},l($){e=b($,"ARTICLE",{class:!0});var L=S(e);t=b(L,"FIGURE",{class:!0});var j=S(t);p&&p.l(j),j.forEach(m),s=O(L),r=b(L,"DIV",{});var G=S(r);n=b(G,"HGROUP",{});var E=S(n);u=b(E,"H5",{class:!0});var K=S(u);i=R(K,o),K.forEach(m),f=O(E),w&&w.l(E),h=O(E),k&&k.l(E),E.forEach(m),G.forEach(m),a=O(L),_=b(L,"DIV",{class:!0});var T=S(_);q&&q.l(T),T.forEach(m),L.forEach(m),this.h()},h(){d(t,"class","full-width flex-grow svelte-zdk8qr"),d(u,"class","text svelte-zdk8qr"),d(_,"class","end full-width svelte-zdk8qr"),d(e,"class","flex svelte-zdk8qr")},m($,L){I($,e,L),c(e,t),p&&p.m(t,null),c(e,s),c(e,r),c(r,n),c(n,u),c(u,i),c(n,f),w&&w.m(n,null),c(n,h),k&&k.m(n,null),c(e,a),c(e,_),q&&q.m(_,null),v=!0},p($,[L]){$[0].formats["image/jpeg"]?p?p.p($,L):(p=Be($),p.c(),p.m(t,null)):p&&(p.d(1),p=null),(!v||L&1)&&o!==(o=$[0].title+"")&&W(i,o),$[0].authors.length>0?w?w.p($,L):(w=Re($),w.c(),w.m(n,h)):w&&(w.d(1),w=null),$[0].languages.length>0?k?k.p($,L):(k=Ae($),k.c(),k.m(n,null)):k&&(k.d(1),k=null),q&&q.p&&(!v||L&2)&&We(q,N,$,$[1],v?Ze(N,$[1],L,null):Xe($[1]),null)},i($){v||(M(q,$),v=!0)},o($){z(q,$),v=!1},d($){$&&m(e),p&&p.d(),w&&w.d(),k&&k.d(),q&&q.d($)}}}const Le=l=>l.name,Ue=(l,e)=>l+", "+e,je=(l,e)=>l+", "+e;function ft(l,e,t){let{$$slots:s={},$$scope:r}=e,{book:n}=e;return l.$$set=u=>{"book"in u&&t(0,n=u.book),"$$scope"in u&&t(1,r=u.$$scope)},[n,r,s]}class ht extends ne{constructor(e){super(),oe(this,e,ft,it,le,{book:0})}}function Qe(l,e,t){const s=l.slice();return s[7]=e[t],s}function _t(l){let e;return{c(){e=B("Error")},l(t){e=R(t,"Error")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function mt(l){let e;return{c(){e=B("Success !")},l(t){e=R(t,"Success !")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function pt(l){let e;return{c(){e=B("Processing")},l(t){e=R(t,"Processing")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function dt(l){let e;return{c(){e=B("Import")},l(t){e=R(t,"Import")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function gt(l){let e,t,s,r,n;function u(h,a){return h[1].status=="idle"?dt:h[1].status=="processing"?pt:h[1].status=="ok"?mt:_t}let o=u(l),i=o(l);function f(){return l[5](l[7])}return{c(){e=g("button"),i.c(),s=y(),this.h()},l(h){e=b(h,"BUTTON",{"aria-busy":!0,class:!0});var a=S(e);i.l(a),a.forEach(m),s=O(h),this.h()},h(){d(e,"aria-busy",t=l[1].status=="processing"),d(e,"class","full-width svelte-t0qkv2")},m(h,a){I(h,e,a),i.m(e,null),I(h,s,a),r||(n=x(e,"click",f),r=!0)},p(h,a){l=h,o!==(o=u(l))&&(i.d(1),i=o(l),i&&(i.c(),i.m(e,null))),a&2&&t!==(t=l[1].status=="processing")&&d(e,"aria-busy",t)},d(h){h&&(m(e),m(s)),i.d(),r=!1,n()}}}function Fe(l){let e,t;return e=new ht({props:{book:l[7],$$slots:{default:[gt]},$$scope:{ctx:l}}}),{c(){ee(e.$$.fragment)},l(s){te(e.$$.fragment,s)},m(s,r){se(e,s,r),t=!0},p(s,r){const n={};r&1&&(n.book=s[7]),r&1027&&(n.$$scope={dirty:r,ctx:s}),e.$set(n)},i(s){t||(M(e.$$.fragment,s),t=!0)},o(s){z(e.$$.fragment,s),t=!1},d(s){re(e,s)}}}function bt(l){let e,t,s,r="Search Public Domain Books",n,u,o,i,f,h,a,_=l[0].status=="processing"?"Processing":"Search",v,p,w,k,N,q,$,L,j,G=he(l[0].results),E=[];for(let T=0;T<G.length;T+=1)E[T]=Fe(Qe(l,G,T));const K=T=>z(E[T],1,1,()=>{E[T]=null});return q=new we({props:{message:l[1].error}}),{c(){e=g("section"),t=g("article"),s=g("h4"),s.textContent=r,n=y(),u=g("hr"),o=y(),i=g("form"),f=g("input"),h=y(),a=g("button"),v=B(_),w=y(),k=g("div");for(let T=0;T<E.length;T+=1)E[T].c();N=y(),ee(q.$$.fragment),this.h()},l(T){e=b(T,"SECTION",{id:!0});var A=S(e);t=b(A,"ARTICLE",{});var U=S(t);s=b(U,"H4",{"data-svelte-h":!0}),fe(s)!=="svelte-16fk5mr"&&(s.textContent=r),n=O(U),u=b(U,"HR",{}),o=O(U),i=b(U,"FORM",{});var P=S(i);f=b(P,"INPUT",{type:!0,name:!0,placeholder:!0,"aria-label":!0}),h=O(P),a=b(P,"BUTTON",{"aria-busy":!0,class:!0});var X=S(a);v=R(X,_),X.forEach(m),P.forEach(m),w=O(U),k=b(U,"DIV",{class:!0});var J=S(k);for(let Y=0;Y<E.length;Y+=1)E[Y].l(J);J.forEach(m),N=O(U),te(q.$$.fragment,U),U.forEach(m),A.forEach(m),this.h()},h(){d(f,"type","search"),d(f,"name","search"),d(f,"placeholder","Search Book"),d(f,"aria-label","Search"),d(a,"aria-busy",p=l[0].status=="processing"),d(a,"class","full-width svelte-t0qkv2"),d(k,"class","grid overflow-auto svelte-t0qkv2"),d(e,"id","search-form")},m(T,A){I(T,e,A),c(e,t),c(t,s),c(t,n),c(t,u),c(t,o),c(t,i),c(i,f),Z(f,l[0].search),c(i,h),c(i,a),c(a,v),c(t,w),c(t,k);for(let U=0;U<E.length;U+=1)E[U]&&E[U].m(k,null);c(t,N),se(q,t,null),$=!0,L||(j=[x(f,"input",l[4]),x(a,"click",l[2])],L=!0)},p(T,[A]){if(A&1&&f.value!==T[0].search&&Z(f,T[0].search),(!$||A&1)&&_!==(_=T[0].status=="processing"?"Processing":"Search")&&W(v,_),(!$||A&1&&p!==(p=T[0].status=="processing"))&&d(a,"aria-busy",p),A&11){G=he(T[0].results);let P;for(P=0;P<G.length;P+=1){const X=Qe(T,G,P);E[P]?(E[P].p(X,A),M(E[P],1)):(E[P]=Fe(X),E[P].c(),M(E[P],1),E[P].m(k,null))}for(ke(),P=G.length;P<E.length;P+=1)K(P);ve()}const U={};A&2&&(U.message=T[1].error),q.$set(U)},i(T){if(!$){for(let A=0;A<G.length;A+=1)M(E[A]);M(q.$$.fragment,T),$=!0}},o(T){E=E.filter(Boolean);for(let A=0;A<E.length;A+=1)z(E[A]);z(q.$$.fragment,T),$=!1},d(T){T&&m(e),be(E,T),re(q),L=!1,De(j)}}}function kt(l,e,t){const s=Me();let r={search:"",status:"idle",results:[]},n={status:"idle",error:""};async function u(){t(0,r.status="processing",r),t(1,n.status="idle",n),t(1,n.error="",n),t(0,r.results=[],r);const h="https://gutendex.com/books?search="+r.search.replaceAll(" ","%20"),a=await fetch(h,{method:"GET"}),_=await a.json();if(a.ok&&_.results.length>0)t(0,r.results=_.results,r),t(0,r.status="ok",r);else throw new Error(a.statusText)}async function o(h){t(1,n.status="processing",n),t(1,n.error="",n),t(0,r.results=[h],r);const a=await fetch("import-book",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(h)}),_=await a.json();a.ok?(t(1,n.status="ok",n),setTimeout(()=>{t(0,r.results=[],r)},3e3),s("new-book")):(t(1,n.status="error",n),t(1,n.error=_?JSON.stringify(_):a.statusText,n))}function i(){r.search=this.value,t(0,r)}return[r,n,u,o,i,h=>o(h)]}class vt extends ne{constructor(e){super(),oe(this,e,kt,bt,le,{})}}function wt(l){let e,t,s=l[4].message+"",r,n;return{c(){e=g("span"),t=B('Server unavailable: "'),r=B(s),n=B('"')},l(u){e=b(u,"SPAN",{});var o=S(e);t=R(o,'Server unavailable: "'),r=R(o,s),n=R(o,'"'),o.forEach(m)},m(u,o){I(u,e,o),c(e,t),c(e,r),c(e,n)},p:ie,d(u){u&&m(e)}}}function Et(l){let e,t,s,r,n,u,o;function i(a,_){return a[0].status=="idle"?Ct:a[0].status=="processing"?St:a[0].status=="ok"?Tt:$t}let f=i(l),h=f(l);return{c(){e=g("form"),t=g("input"),s=y(),r=g("button"),h.c(),this.h()},l(a){e=b(a,"FORM",{});var _=S(e);t=b(_,"INPUT",{type:!0,id:!0,name:!0,accept:!0}),s=O(_),r=b(_,"BUTTON",{"aria-busy":!0,class:!0});var v=S(r);h.l(v),v.forEach(m),_.forEach(m),this.h()},h(){d(t,"type","file"),d(t,"id","file"),d(t,"name","file"),d(t,"accept",".epub"),d(r,"aria-busy",n=l[0].status=="processing"),d(r,"class","full-width svelte-1p1u34")},m(a,_){I(a,e,_),c(e,t),c(e,s),c(e,r),h.m(r,null),u||(o=x(r,"click",l[1]),u=!0)},p(a,_){f!==(f=i(a))&&(h.d(1),h=f(a),h&&(h.c(),h.m(r,null))),_&1&&n!==(n=a[0].status=="processing")&&d(r,"aria-busy",n)},d(a){a&&m(e),h.d(),u=!1,o()}}}function $t(l){let e;return{c(){e=B("Error")},l(t){e=R(t,"Error")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function Tt(l){let e;return{c(){e=B("Success !")},l(t){e=R(t,"Success !")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function St(l){let e;return{c(){e=B("Processing")},l(t){e=R(t,"Processing")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function Ct(l){let e;return{c(){e=B("Upload")},l(t){e=R(t,"Upload")},m(t,s){I(t,e,s)},d(t){t&&m(e)}}}function qt(l){let e,t="Checking server status...";return{c(){e=g("span"),e.textContent=t,this.h()},l(s){e=b(s,"SPAN",{"aria-busy":!0,"data-svelte-h":!0}),fe(e)!=="svelte-r6f49d"&&(e.textContent=t),this.h()},h(){d(e,"aria-busy","true")},m(s,r){I(s,e,r)},p:ie,d(s){s&&m(e)}}}function Pt(l){let e,t,s,r="Import Epub Files",n,u,o,i,f,h,a={ctx:l,current:null,token:null,hasCatch:!0,pending:qt,then:Et,catch:wt,value:3,error:4};return et(yt(),a),f=new we({props:{message:l[0].error}}),{c(){e=g("section"),t=g("article"),s=g("h4"),s.textContent=r,n=y(),u=g("hr"),o=y(),a.block.c(),i=y(),ee(f.$$.fragment),this.h()},l(_){e=b(_,"SECTION",{id:!0});var v=S(e);t=b(v,"ARTICLE",{});var p=S(t);s=b(p,"H4",{"data-svelte-h":!0}),fe(s)!=="svelte-tnb7qc"&&(s.textContent=r),n=O(p),u=b(p,"HR",{}),o=O(p),a.block.l(p),i=O(p),te(f.$$.fragment,p),p.forEach(m),v.forEach(m),this.h()},h(){d(e,"id","upload-form")},m(_,v){I(_,e,v),c(e,t),c(t,s),c(t,n),c(t,u),c(t,o),a.block.m(t,a.anchor=null),a.mount=()=>t,a.anchor=i,c(t,i),se(f,t,null),h=!0},p(_,[v]){l=_,tt(a,l,v);const p={};v&1&&(p.message=l[0].error),f.$set(p)},i(_){h||(M(f.$$.fragment,_),h=!0)},o(_){z(f.$$.fragment,_),h=!1},d(_){_&&m(e),a.block.d(),a.token=null,a=null,re(f)}}}async function yt(){const l=await fetch("status",{method:"GET"}),e=await l.json();if(l.ok&&e.status)return e.status;throw new Error(l.statusText)}function Ot(l,e,t){const s=Me();let r={status:"idle",error:""};async function n(){t(0,r.status="processing",r),t(0,r.error="",r);const u=document.getElementById("file"),o=new FormData;u.files&&o.append("file",u.files[0]);try{const i=await fetch("upload-file",{method:"POST",body:o}),f=await i.json();i.ok?(t(0,r.status="ok",r),s("new-book")):t(0,r.error=f?JSON.stringify(f):i.statusText,r)}catch(i){t(0,r.error=String(i),r)}}return[r,n]}class It extends ne{constructor(e){super(),oe(this,e,Ot,Pt,le,{})}}function Nt(l){let e,t,s,r,n,u;return e=new ct({props:{books:l[0]}}),s=new vt({}),s.$on("new-book",l[1]),n=new It({}),n.$on("new-book",l[1]),{c(){ee(e.$$.fragment),t=y(),ee(s.$$.fragment),r=y(),ee(n.$$.fragment)},l(o){te(e.$$.fragment,o),t=O(o),te(s.$$.fragment,o),r=O(o),te(n.$$.fragment,o)},m(o,i){se(e,o,i),I(o,t,i),se(s,o,i),I(o,r,i),se(n,o,i),u=!0},p(o,[i]){const f={};i&1&&(f.books=o[0]),e.$set(f)},i(o){u||(M(e.$$.fragment,o),M(s.$$.fragment,o),M(n.$$.fragment,o),u=!0)},o(o){z(e.$$.fragment,o),z(s.$$.fragment,o),z(n.$$.fragment,o),u=!1},d(o){o&&(m(t),m(r)),re(e,o),re(s,o),re(n,o)}}}function Bt(l,e,t){let s=[];xe(r);async function r(){var n;try{const u=await fetch("books",{method:"GET"}),o=await u.json();u.ok&&((n=o.books)==null?void 0:n.length)>0&&t(0,s=o.books)}catch(u){console.error("Fetch error:",u)}}return[s,r]}class Lt extends ne{constructor(e){super(),oe(this,e,Bt,Nt,le,{})}}export{Lt as component};