import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'

import './index.css'
import { OutputProps } from './types'

export default function Output({ value }: OutputProps) {
    return ( 
        <div href="#" className="output border border-gray-200 shadow p-3">
            {value}
        </div>
    )
}