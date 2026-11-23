import type React from "react";
import Nav from "./dashboardComponents/Nav";
import ProjectBox from "./dashboardComponents/ProjectBox";
import SearchBar from "./dashboardComponents/SearchBar";
import UploadBox from "./dashboardComponents/Upload/UploadBox";

type HomeProps = {
  uploadImg: boolean;
  setUploadImg: React.Dispatch<React.SetStateAction<boolean>>;
  image: File | null;
  setImage: React.Dispatch<React.SetStateAction<File | null>>;
};

const Home: React.FC<HomeProps> = ({
  uploadImg,
  setUploadImg,
  image,
  setImage,
}) => {
  return (
    <>
      <Nav setUploadImg={setUploadImg} />
      <SearchBar />
      <ProjectBox />
      <UploadBox
        uploadImg={uploadImg}
        setUploadImg={setUploadImg}
        image={image}
        setImage={setImage}
      />
    </>
  );
};

export default Home;
