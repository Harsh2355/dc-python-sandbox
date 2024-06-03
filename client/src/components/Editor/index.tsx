import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom';

import Editor from '@monaco-editor/react';

import { DEFAULT_MESSAGE } from './constants'
import { EditorProps } from './types';

export default function PythonEditor({ update }: EditorProps) {

    const [text, setText] = useState<string>(DEFAULT_MESSAGE)

    // Effect to load the saved text from session storage when the component mounts
    useEffect(() => {
        const savedText: string = sessionStorage.getItem('savedText');
        console.log(savedText)
        if (savedText != '') {
            update(savedText)
            setText(savedText)
        }
    }, []);

    const handleEditorChange = (value: string, event: Event) => {
        sessionStorage.setItem('savedText', value);
        update(value)
    }

    return (
        <div>
            <Editor 
                width="60vw" 
                height="65vh" 
                defaultLanguage="python"
                theme="vs-dark"
                defaultValue={text}
                onChange={handleEditorChange} />
        </div>
    )
}