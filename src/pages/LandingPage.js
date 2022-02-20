import React, { useEffect, useState }  from "react";
import httpClient from "../httpClient";
import '../index.css'

const LandingPage = () => {
    const [user,setUser] = useState(null)

    const logoutUser = async () => {
        const resp = await httpClient.post('//localhost:5000/logout');
        window.location.href = '/'

    }

    useEffect( ()=>{
       (async ()=>{
            try{
                const resp = await httpClient.get('//localhost:5000/@me')
                setUser(resp.data)
            }catch(error){
                console.log('not auth')
            }

       })()
    },[])
        
       
    return(
        <div>
           {user != null ? (
            <div>
                <h1>Logged in</h1>
                <h2>ID:{user.id}</h2>
                <h3>Email:{user.email}</h3>
                <button onClick={logoutUser}>Logout</button>
           </div>

           
           ) : (
               <div>
                    <h1>Login Page</h1>
                    <p>You are not login</p>
                    <a href="/login"><button className="buttonone">Login</button></a>
                    <a href="/register"><button>Register</button></a>
               </div>
           )}
        </div>
    )
}

export default LandingPage