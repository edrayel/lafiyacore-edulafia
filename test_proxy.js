const axios = require('axios');
async function run() {
  try {
    const res = await axios.post('http://localhost:5173/api/v1/auth/login', {
      email: 'admin@edulafia.com',
      password: 'Admin123!'
    });
    console.log('Login success:', res.status);
    const cookies = res.headers['set-cookie'];
    console.log('Cookies:', cookies);
    const me = await axios.get('http://localhost:5173/api/v1/auth/me', {
      headers: { Cookie: cookies.join(';') }
    });
    console.log('Me success:', me.status);
  } catch (e) {
    console.error('Error:', e.response ? e.response.status : e.message);
  }
}
run();
