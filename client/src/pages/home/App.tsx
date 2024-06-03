import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { DEFAULT_MESSAGE, WAITING_MESSAAGE } from "./constants";
import postRequest from "../../api/apiService";
import Header from "../../components/Header";
import PythonEditor from "../../components/Editor";
import Output from "../../components/Output";

function App() {
  const [output, setOutput] = useState<string>(DEFAULT_MESSAGE);
  const [editorText, setEditorText] = useState<string>("");

  const updateEditorText = (new_text) => {
    setEditorText(new_text);
  };

  const handleTestCode = async () => {
    setOutput(WAITING_MESSAAGE);

    // send editor text to api so it can execute
    const { data, error } = await postRequest("/test-code", {
      code: editorText,
    });

    setOutput(data.message);
  };

  const handleSubmit = async () => {
    setOutput(WAITING_MESSAAGE);

    // send editor text to api so it can execute
    const { data, error } = await postRequest("/submit", {
      code: editorText,
    });

    setOutput(data.message);
  };

  return (
    <>
      <div className="min-h-screen min-w-full app-container">
        <div className="p-6">
          <Header handleTestCode={handleTestCode} handleSubmit={handleSubmit} />
        </div>
        <div className="flex">
          <div className="w-3/5 pt-1 pb-6 pl-6 pr-6">
            <PythonEditor update={updateEditorText} />
          </div>
          <div className="w-2/5 pt-1 pb-6 pl-6 pr-6">
            <Output value={output} />
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
