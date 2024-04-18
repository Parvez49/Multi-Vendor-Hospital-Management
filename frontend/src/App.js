import React from 'react';
import FormInput from './components/Form/FormInput';
// import { useDispatch, useSelector } from 'react-redux';
import { useState, useEffect } from 'react';
// import {login, reset} from '../features/auth/authSlice';
import { useNavigate } from 'react-router-dom';
import axios from "axios";



const BACKEND_DOMAIN = "http://127.0.0.1:8000";
const LOGIN_URL = `${BACKEND_DOMAIN}/accounts/login`

const Login = () => {

    const inputs = [
        {
            id:1,
            name:"email",
            type:"email",
            placeholder:"Email",
            errorMessage:"It should be valid email address",
            label:"Email",
            required:true,
        },
        {
            id:2,
            name:"password",
            type:"password",
            placeholder:"Password",
            errorMessage: "Password should be 8-20 characters and include at least 1 letter, 1 number and 1 special character!",
            label:"Password",
            //pattern: `^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,20}$`,
            reqired:true
        }
        
    ]

    const [formData,setFormData] =useState({
        email:'',
        password:''
    })  

    const handleChange=(e)=>{
        setFormData({
            ...formData,
            [e.target.name]:e.target.value
        })
    }
    const handleSubmit = async (e)=>{
        e.preventDefault()
        const response = await axios.post(LOGIN_URL,formData)
        if (response.data){
            console.log(response.data)
            alert("Login Successful")
        }

    }

    return (
        <div className='app flex items-center justify-center h-screen bg-cover bg-center bg-gradient-to-br from-transparent to-transparent ' style={{backgroundImage: "url('https://images.pexels.com/photos/114979/pexels-photo-114979.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500')"}}>
            <form onSubmit={handleSubmit} className='form bg-white py-0 px-5 rounded-md'>
                <h1 className='text-purple-800 text-center text-2xl font-bold mt-5'>Login</h1>
                {inputs.map((input)=>(
                    <FormInput 
                        key={input.id}
                        {...input}
                        value={formData[input.name]}
                        onChange={handleChange}

                    />
                ))}
                <button className='button bg-purple-500 text-white w-full p-2 rounded-md font-bold text-lg cursor-pointer mt-5 mb-8'>Submit</button>
            </form>
            
        </div>
    );
};

export default Login;