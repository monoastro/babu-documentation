import { Routes, Route } from "react-router-dom";
import { useState } from "react";
import Home from "./component/Dashboard/home";
import EditorPage from "./component/editor/EditorPage";

function App() {
  const [uploadImg, setUploadImg] = useState(false);
  const [image, setImage] = useState<File | null>(null);

  return (
    <>
      <Routes>
        <Route
          path="/"
          element={
            <Home
              uploadImg={uploadImg}
              setUploadImg={setUploadImg}
              image={image}
              setImage={setImage}
            />
          }
        />
        <Route path="/editor" element={<EditorPage />} />
      </Routes>
    </>
  );
}

export default App;
