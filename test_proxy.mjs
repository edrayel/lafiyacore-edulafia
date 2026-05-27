async function run() {
  try {
    const res = await fetch('http://localhost:5174/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: 'admin@edulafia.com',
        password: 'Admin123!'
      })
    });
    console.log('Login success:', res.status);
    
    // Parse cookies correctly
    const cookieHeader = res.headers.get('set-cookie');
    const cookies = cookieHeader.split(',').map(c => c.split(';')[0].trim()).join('; ');
    
    console.log('Parsed Cookies:', cookies);
    const me = await fetch('http://localhost:5174/api/v1/auth/me', {
      headers: { Cookie: cookies }
    });
    console.log('Me success:', me.status);
    const body = await me.text();
    console.log('Me body:', body);
  } catch (e) {
    console.error('Error:', e.message);
  }
}
run();
