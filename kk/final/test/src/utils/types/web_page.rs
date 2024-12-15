/// This enum defines the possible web pages to be opened.
#[derive(Debug, Clone)]
pub enum WebPage {
   
    IssueLanguages,
    Wiki,
}

impl WebPage {
    pub fn get_url(&self) -> &str {
        match self {
         
            
            WebPage::IssueLanguages => "https://github.com/GyulyVGC/sniffnet/issues/60",
            WebPage::Wiki => "https://github.com/GyulyVGC/sniffnet/wiki",
        }
    }
}
