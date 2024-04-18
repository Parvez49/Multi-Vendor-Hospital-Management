import React, {useState} from 'react';

const FormInput = (props) => {

    const {id,label,errorMessage,onChange,isValid,...inputProps} = props

    
    return (
        <div className='input flex flex-col'>
            <label className='text-md text-gray-400'>{label}</label>
            <input className='p-3 mt-2 mb-2 rounded-md border border-solid border-gray-300'
                {...inputProps}
                onChange={onChange}
            />
        
        {/* {!isValid && isFocused && (<span className='error text-sm p-1 text-red-600 border-none'>{errorMessage}</span>)} */}
        </div>
    );
};

export default FormInput;