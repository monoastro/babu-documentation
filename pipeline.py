
class processing_pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, data):
        for step in self.steps:
            data = step.process(data)
        return data
    
    def llmcall(self,data):
        prompt=''
        

    def preprocessing(self,data):
        pass

    def text_extraction(self,img_data):
        text=self.llmcall(img_data)
        return text



class data_merging:

    def __init__(self, data1, data2):
        self.data1=data1 #ocr/llm output  for text #azure
        self.data2=data2 ##ocr/llm output for numbers #tesseract

    def merge(self):
        #if text give priority to azure output
        #for number give priority to tesseract

        merged_data={}
        for key in self.data1:
            if key in self.data2:
                if isinstance(self.data1[key], str) and self.data1[key].isalpha():
                    merged_data[key] = self.data1[key]
                elif isinstance(self.data2[key], str) and self.data2[key].isdigit():
                    merged_data[key] = self.data2[key]
                else:
                    merged_data[key] = self.data1[key]  # Default to data1 if no clear priority
            else:
                merged_data[key] = self.data1[key]



# the merged output is fed to html generator that generates final rendered output translated  

class html_generator: 
    pass




    
    

