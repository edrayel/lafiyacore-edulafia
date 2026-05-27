async function run() {
  const res = await fetch('http://localhost:5173/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email: 'admin@edulafia.com', password: 'Admin123!' })
  });
  const cookies = res.headers.get('set-cookie')?.split(',').map(c => c.split(';')[0].trim()).join('; ');
  if (!cookies) {
     console.log("No cookies:", await res.text());
     return;
  }
  const me = await fetch('http://localhost:5173/api/v1/auth/me', { headers: { Cookie: cookies } });
  const user = await me.json();
  
  if (user.school_id) {
    const dash = await fetch(`http://localhost:5173/api/v1/intelligence/school/${user.school_id}/dashboard`, { headers: { Cookie: cookies } });
    console.log("Dash Status:", dash.status);
    console.log("Dash Body:", await dash.text());
  } else {
    console.log("No school_id on user", user);
  }
}
run();
