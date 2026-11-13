import {useEffect,useState} from 'react';
import {api} from './services/api';
import {useCart} from './hooks/useCart';

import {ShoppingBag,Search,Plus,Minus,Trash2,X,ShieldCheck,LogIn,LogOut,PackageCheck,LayoutDashboard,ClipboardList,Box,RefreshCw,Edit3,ChevronRight} from 'lucide-react';

const money=n=>new Intl.NumberFormat('es-CO',{style:'currency',currency:'COP',maximumFractionDigits:0}).format(Number(n)||0);

const blank={name:'',description:'',price:'',stock:'',category:'General',image_url:''};

const demo=[{id:1,name:'Audífonos Studio',description:'Sonido envolvente para tu día.',price:189900,stock:12,category:'Tecnología',image_url:'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=900'},{id:2,name:'Reloj Minimal',description:'Diseño limpio para cualquier ocasión.',price:129900,stock:8,category:'Accesorios',image_url:'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=900'},{id:3,name:'Mochila Urbana',description:'Espacio y comodidad para moverte.',price:159900,stock:5,category:'Accesorios',image_url:'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=900'}];


export default function App(){
 const[products,setProducts]=useState([]),[query,setQuery]=useState(''),[drawer,setDrawer]=useState(false),[auth,setAuth]=useState(false),[mode,setMode]=useState('login'),[form,setForm]=useState({name:'',email:'',password:''}),[token,setToken]=useState(()=>localStorage.getItem('nexo_token')||''),[user,setUser]=useState(()=>JSON.parse(localStorage.getItem('nexo_user')||'null')),[notice,setNotice]=useState(''),[busy,setBusy]=useState(false),[view,setView]=useState('shop'),[summary,setSummary]=useState(null),[orders,setOrders]=useState([]),[productForm,setProductForm]=useState(blank),[editing,setEditing]=useState(null);

 const {items:cart,count,total,add:addToCart,changeQuantity,remove:removeFromCart,clear:clearCart}=useCart();

 async function load() {
    try {
      setProducts(await api.getProducts());
    } catch {
      setProducts(demo);
    }
  }

  async function loadAdmin() {
    if (!token || user?.role !== 'admin') return;

    try {
      const [adminSummary, adminOrders] = await Promise.all([
        api.getAdminSummary(token),
        api.getAdminOrders(token),
      ]);
      setSummary(adminSummary);
      setOrders(adminOrders);
    } catch {
      setNotice('No fue posible cargar el panel administrativo');
    }
  }

  async function loadOrders() {
    if (!token) return;

    try {
      setOrders(await api.getMyOrders(token));
    } catch {
      setNotice('No fue posible cargar tus pedidos');
    }
  }

  useEffect(()=>{load()},[]);

 useEffect(() => {
    if (!token) return;

    api.getCurrentUser(token)
      .then((currentUser) => {
        setUser(currentUser);
        localStorage.setItem('nexo_user', JSON.stringify(currentUser));
      })
      .catch(() => logout());
  }, [token]);

 useEffect(()=>{if(notice){const t=setTimeout(()=>setNotice(''),3500);
return()=>clearTimeout(t)}},[notice]);

 useEffect(()=>{if(view==='admin')loadAdmin();
if(view==='orders')loadOrders()},[view,token]);

 const filtered=products.filter(p=>(p.name+' '+p.category).toLowerCase().includes(query.toLowerCase()));

 function add(product) {
    const result = addToCart(product);
    setNotice(result.message);
  }

async function authSubmit(e) {
    e.preventDefault();
    setBusy(true);

    try {
      if (mode === 'register') {
        await api.register(form);
        setMode('login');
        setNotice('Cuenta creada. Ahora inicia sesión.');
        return;
      }

      const data = await api.login(form.email, form.password);
      localStorage.setItem('nexo_token', data.access_token);
      localStorage.setItem('nexo_user', JSON.stringify(data.user));
      setToken(data.access_token);
      setUser(data.user);
      setAuth(false);
      setNotice('¡Hola, ' + data.user.name + '!');
    } catch (error) {
      setNotice(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function checkout() {
    if (!token) {
      setAuth(true);
      setDrawer(false);
      setNotice('Inicia sesión para finalizar tu compra');
      return;
    }

    setBusy(true);
    try {
      const items = cart.map((product) => ({
        product_id: product.id,
        quantity: product.quantity,
      }));
      const order = await api.checkout(items, token);
      clearCart();
      setDrawer(false);
      setNotice('¡Compra confirmada! Pedido #' + order.id);
      await load();
    } catch (error) {
      setNotice(error.message);
      await load();
    } finally {
      setBusy(false);
    }
  }

  function logout(){localStorage.removeItem('nexo_token');
localStorage.removeItem('nexo_user');
setToken('');
setUser(null);
setView('shop');
setNotice('Sesión cerrada')}

function editProduct(p){setEditing(p.id);
setProductForm({name:p.name,description:p.description,price:String(p.price),stock:String(p.stock),category:p.category,image_url:p.image_url||''});
window.scrollTo({top:0,behavior:'smooth'})}

async function saveProduct(e) {
    e.preventDefault();
    setBusy(true);

    try {
      const payload = {
        ...productForm,
        price: Number(productForm.price),
        stock: Number(productForm.stock),
      };
      await api.saveProduct(payload, editing, token);
      setNotice(editing ? 'Producto actualizado' : 'Producto creado');
      setProductForm(blank);
      setEditing(null);
      await load();
      await loadAdmin();
    } catch (error) {
      setNotice(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function deleteProduct(id) {
    if (!window.confirm('¿Seguro que deseas eliminar este producto?')) return;

    try {
      await api.deleteProduct(id, token);
      setNotice('Producto eliminado');
      await load();
      await loadAdmin();
    } catch (error) {
      setNotice(error.message);
    }
  }

  return (
    <div className="shell">
 <header>
<a className="brand" href="#" onClick={()=>setView('shop')}>
<b>N</b> nexo<span>shop.</span>
</a>
<nav>
<a href="#catalogo" onClick={()=>setView('shop')}>Catálogo</a>
<a href="#promesa">Nuestra promesa</a>{user&&<a href="#orders" onClick={()=>setView('orders')}>Mis pedidos</a>}{user?.role==='admin'&&<a href="#admin" onClick={()=>setView('admin')}>Administración</a>}</nav>
<div className="actions">{user?<>
<small>Hola, {user.name.split(' ')[0]}</small>
<button className="plain" onClick={logout}>
<LogOut size={17}/>
</button>
</>:<button className="plain" onClick={()=>setAuth(true)}>
<LogIn size={17}/> Ingresar</button>}<button className="cart-button" onClick={()=>setDrawer(true)}>
<ShoppingBag size={18}/> Carrito <b>{count}</b>
</button>
</div>
</header>
 {view==='shop'&&<main>
<section className="hero">
<div>
<label>✦ NUEVA EXPERIENCIA DE COMPRA</label>
<h1>Lo que buscas,<br/>
<i>más cerca.</i>
</h1>
<p>Productos que hacen tu día mejor. Descubre una selección pensada para ti, con una compra simple y segura.</p>
<a className="cta" href="#catalogo">Explorar productos ↗</a>
<div className="trust">
<span>
<ShieldCheck/> Compra protegida</span>
<span>
<PackageCheck/> Stock en tiempo real</span>
</div>
</div>
<div className="hero-image">
<img src="https://images.unsplash.com/photo-1490312278390-ab64016e0aa9?w=1100" alt="Selección de productos"/>
<div className="floating">
<b>✦</b>
<span>Tu próxima elección<small>Está a un clic de distancia</small>
</span>
</div>
</div>
</section>
<section className="catalog" id="catalogo">
<div className="heading">
<div>
<label>SELECCIÓN NEXO</label>
<h2>Encuentra tu <i>siguiente favorito.</i>
</h2>
</div>
<div className="search">
<Search/>
<input placeholder="Buscar productos..." value={query} onChange={e=>setQuery(e.target.value)}/>
</div>
</div>
<div className="grid">{filtered.map((p,i)=>
<article className="product" key={p.id}>
<div className="photo">
<img src={p.image_url||demo[i%demo.length].image_url} alt={p.name}/>
<span>{p.category}</span>
<button onClick={()=>add(p)} disabled={!p.stock}>
<Plus/>
</button>
</div>
<h3>{p.name}</h3>
<p>{p.description}</p>
<div className="price">
<b>{money(p.price)}</b>
<small>{p.stock?p.stock+' disponibles':'Agotado'}</small>
</div>
</article>)}</div>{!filtered.length&&<p className="empty">No encontramos productos con esa búsqueda.</p>}</section>
<section className="promise" id="promesa">
<div>
<label>COMPRAR DEBERÍA SER SIMPLE</label>
<h2>Una experiencia<br/>
<i>sin complicaciones.</i>
</h2>
</div>
<div>
<ShieldCheck/>
<b>Compra segura</b>
<p>Tu cuenta y tus datos están protegidos.</p>
</div>
<div>
<PackageCheck/>
<b>Inventario real</b>
<p>Confirmamos disponibilidad antes de cada pedido.</p>
</div>
<div>
<ShoppingBag/>
<b>Todo en un lugar</b>
<p>Compra fácil y consulta tus pedidos.</p>
</div>
</section>
</main>}
 {view==='orders'&&<main className="workspace">
<div className="workspace-title">
<div>
<label>MI CUENTA</label>
<h1>Mis pedidos</h1>
<p>Consulta el estado y el detalle de tus compras.</p>
</div>
<button className="plain" onClick={()=>setView('shop')}>Volver a la tienda <ChevronRight/>
</button>
</div>{orders.length?<div className="orders-list">{orders.map(o=>
<article className="order-card" key={o.id}>
<div className="order-top">
<b>Pedido #{o.id}</b>
<span className="status">{o.status==='paid'?'Pagado':o.status}</span>
<strong>{money(o.total)}</strong>
</div>{o.items.map(i=>
<div className="order-item" key={i.product_id}>
<span>{i.product_name} × {i.quantity}</span>
<b>{money(i.unit_price*i.quantity)}</b>
</div>)}<small>Referencia de pago: {o.payment_reference}</small>
</article>)}</div>:<div className="empty-state">
<PackageCheck/>
<h3>Aún no tienes pedidos</h3>
<p>Cuando realices tu primera compra, aparecerá aquí.</p>
<button className="cta" onClick={()=>setView('shop')}>Ir al catálogo</button>
</div>}</main>}
 {view==='admin'&&user?.role==='admin'&&<main className="workspace admin-workspace">
<div className="workspace-title">
<div>
<label>GESTIÓN DE LA TIENDA</label>
<h1>Panel de administración</h1>
<p>Controla el catálogo, las existencias y las ventas.</p>
</div>
<button className="plain" onClick={()=>{load();
loadAdmin()}}>
<RefreshCw/> Actualizar</button>
</div>
<div className="stats">{[['Productos',summary?.products??products.length,Box],['Unidades disponibles',summary?.units_in_stock??'—',PackageCheck],['Pedidos',summary?.orders??orders.length,ClipboardList],['Ingresos',money(summary?.revenue??0),ShoppingBag]].map(([label,value,Icon])=>
<div className="stat" key={label}>
<Icon/>
<small>{label}</small>
<b>{value}</b>
</div>)}</div>
<div className="admin-columns">
<section className="admin-form">
<label>{editing?'EDITAR PRODUCTO':'NUEVO PRODUCTO'}</label>
<h2>{editing?'Actualiza el catálogo':'Agregar al catálogo'}</h2>
<form onSubmit={saveProduct}>
<input required minLength="2" placeholder="Nombre del producto" value={productForm.name} onChange={e=>setProductForm({...productForm,name:e.target.value})}/>
<textarea placeholder="Descripción" value={productForm.description} onChange={e=>setProductForm({...productForm,description:e.target.value})}/>
<div className="form-pair">
<input required type="number" min="1" step="1" placeholder="Precio (COP)" value={productForm.price} onChange={e=>setProductForm({...productForm,price:e.target.value})}/>
<input required type="number" min="0" step="1" placeholder="Existencias" value={productForm.stock} onChange={e=>setProductForm({...productForm,stock:e.target.value})}/>
</div>
<input placeholder="Categoría" value={productForm.category} onChange={e=>setProductForm({...productForm,category:e.target.value})}/>
<input type="url" placeholder="URL de imagen (opcional)" value={productForm.image_url} onChange={e=>setProductForm({...productForm,image_url:e.target.value})}/>
<button className="cta full" disabled={busy}>{busy?'Guardando...':editing?'Guardar cambios':'Crear producto'}</button>{editing&&<button type="button" className="plain cancel-edit" onClick={()=>{setEditing(null);
setProductForm(blank)}}>Cancelar edición</button>}</form>
</section>
<section className="admin-products">
<label>INVENTARIO</label>
<h2>Productos registrados</h2>{products.map(p=>
<div className="admin-product" key={p.id}>
<img src={p.image_url||demo[0].image_url} alt=""/>
<div>
<b>{p.name}</b>
<small>{money(p.price)} · {p.stock} unidades</small>
</div>
<button className="plain" title="Editar" onClick={()=>editProduct(p)}>
<Edit3 size={17}/>
</button>
<button className="plain danger" title="Eliminar" onClick={()=>deleteProduct(p.id)}>
<Trash2 size={17}/>
</button>
</div>)}</section>
</div>
<section className="admin-orders">
<label>ACTIVIDAD COMERCIAL</label>
<h2>Últimos pedidos</h2>{orders.length?orders.slice(0,8).map(o=>
<div className="admin-order" key={o.id}>
<b>Pedido #{o.id}</b>
<span>{o.items.reduce((a,x)=>a+x.quantity,0)} artículos</span>
<span className="status">{o.status}</span>
<strong>{money(o.total)}</strong>
</div>):<p className="empty">Todavía no hay pedidos registrados.</p>}</section>
</main>}
 <footer>
<a className="brand" href="#">
<b>N</b> nexo<span>shop.</span>
</a>
<small>© 2026 NexoShop · Proyecto académico</small>
<small>Hecho para comprar mejor.</small>
</footer>
 {notice&&<div className="toast">{notice}</div>}
 {drawer&&<div className="overlay" onMouseDown={e=>e.target===e.currentTarget&&setDrawer(false)}>
<aside className="drawer">
<div className="drawer-head">
<div>
<label>TU SELECCIÓN</label>
<h2>Tu carrito ({count})</h2>
</div>
<button className="plain" onClick={()=>setDrawer(false)}>
<X/>
</button>
</div>{!cart.length?<div className="empty-cart">
<ShoppingBag/>
<b>Tu carrito está esperando.</b>
<p>Agrega algo que te guste y aparecerá aquí.</p>
<button className="cta" onClick={()=>setDrawer(false)}>Seguir explorando</button>
</div>:<>
<div className="lines">{cart.map(p=>
<div className="line" key={p.id}>
<img src={p.image_url} alt=""/>
<div>
<b>{p.name}</b>
<strong>{money(p.price)}</strong>
<div className="quantity">
<button onClick={()=>changeQuantity(p.id,-1)}>
<Minus/>
</button>{p.quantity}<button onClick={()=>changeQuantity(p.id,1)}>
<Plus/>
</button>
<button className="remove" onClick={()=>removeFromCart(p.id)}>
<Trash2/>
</button>
</div>
</div>
</div>)}</div>
<div className="checkout">
<div>
<span>Subtotal</span>
<b>{money(total)}</b>
</div>
<small>Envío calculado en el siguiente paso.</small>
<button className="cta full" disabled={busy} onClick={checkout}>{busy?'Procesando...':'Finalizar compra · '+money(total)}</button>
<p>
<ShieldCheck/> Pago de demostración</p>
</div>
</>}</aside>
</div>}
 {auth&&<div className="overlay" onMouseDown={e=>e.target===e.currentTarget&&setAuth(false)}>
<div className="modal">
<button className="close plain" onClick={()=>setAuth(false)}>
<X/>
</button>
<label>BIENVENIDO A NEXOSHOP</label>
<h2>{mode==='login'?'Qué bueno tenerte de vuelta.':'Crea tu cuenta.'}</h2>
<p>{mode==='login'?'Ingresa para continuar con tu compra.':'Unos pocos datos y estarás listo para comprar.'}</p>
<form onSubmit={authSubmit}>{mode==='register'&&<input required placeholder="Nombre completo" value={form.name} onChange={e=>setForm({...form,name:e.target.value})}/>}<input required type="email" placeholder="Correo electrónico" value={form.email} onChange={e=>setForm({...form,email:e.target.value})}/>
<input required minLength="8" type="password" placeholder="Contraseña (mínimo 8 caracteres)" value={form.password} onChange={e=>setForm({...form,password:e.target.value})}/>
<button className="cta full" disabled={busy}>{busy?'Un momento...':mode==='login'?'Iniciar sesión':'Crear cuenta'}</button>
</form>
<button className="switch plain" onClick={()=>setMode(mode==='login'?'register':'login')}>{mode==='login'?'¿No tienes cuenta? Regístrate':'¿Ya tienes cuenta? Inicia sesión'}</button>
</div>
</div>}
 </div>
  );
}
