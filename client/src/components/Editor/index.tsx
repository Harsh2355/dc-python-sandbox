import React, { useState } from 'react'
import ReactDOM from 'react-dom';

import Editor from '@monaco-editor/react';

import { DEFAULT_MESSAGE } from './constants'
import { EditorProps } from './types';

export default function PythonEditor({ update }: EditorProps) {

    const [code, setCode] = useState<string>(DEFAULT_MESSAGE)

    const handleEditorChange = (value: string, event: Event) => {
        setCode(value)
        update(value)
    }

    return (
        <div>
            <Editor 
                width="60vw" 
                height="65vh" 
                defaultLanguage="python"
                theme="vs-dark"
                defaultValue={DEFAULT_MESSAGE}
                onChange={handleEditorChange} />
        </div>
    )
}