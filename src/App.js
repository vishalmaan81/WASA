import React, { useState, useEffect } from 'react';
// import logo from './logo.svg';
import './App.css';
import { Button, Container, TextField } from '@mui/material';
import { makeStyles } from '@material-ui/core';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import Avatar from '@mui/material/Avatar';
import ComputerRoundedIcon from '@mui/icons-material/ComputerRounded';
import Divider from '@mui/material/Divider';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    minHeight: '100vh',
    padding: theme.spacing(2),
  },
  inputField: {
    width: '100%',
    marginBottom: theme.spacing(2),
  },
  buttonContainer: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    marginBottom: theme.spacing(2),
  },
  scanButton: {
    backgroundColor: '#4caf50',
    color: 'white',
    marginRight: theme.spacing(2),
    '&:hover': {
      backgroundColor: '#388e3c',
    },
  },
  activeButton: {
    backgroundColor: '#2196f3',
    '&:hover': {
      backgroundColor: '#1976d2',
    },
  },
  dataContainer: {
    width: '100%',
    padding: theme.spacing(2),
    backgroundColor: 'white',
    borderRadius: theme.spacing(1),
  },
}));


function App() {

  const theme = makeStyles()
  const classes = useStyles(theme);
  // const [currentTime, setCurrentTime] = useState(0);
  const [url, setUrl] = useState("");
  // const [urlCheck, setUrlCheck] = useState({});
  // const [loading, setLoading] = useState(false);
  const [urlCheckResult, setUrlCheckResult] = useState({});
  const[xssResult,setXssResult]= useState({})
  const[networkResult,setNetworkResult]=useState({})
  const[sqliResult,setSqliResult]=useState({})
  // const[printUrlCheckData,setPrintUrlCheckData]=useState(false)

  const[testingXss,setTestingXss]= useState(false)
  const[testingSqli,setTestingSqli]= useState(false)
  const[testingWebTech,setTestingWebTech]= useState(false)
  const[testingNetwork,setTestingNetwork]= useState(false)

  const[xssData,setXssData]=useState()
  const[webTechData,setWebTechData]=useState()
  const[networkData,setNetworkData]=useState()
  const[sqliData,setSqliData]=useState()


  const [activeButton, setActiveButton] = useState(null)

  useEffect(() => {
    console.log("URL changed",url)
    setUrl(url)
  },[url]);
  

// Web Technology scanning =======================================

  const scanWebsiteTech = async () => {
    if (url) {
    // setLoading(true);
    console.log("URL ", url)
    try {
    fetch('/detectTechnologies', {
      method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     },
      body: JSON.stringify({ url })
     })
    .then(response => response.json())
    .then(data => {
      console.log('Response - ', data);
      // Process the received data here
      setUrlCheckResult(data);
    })
    } catch (error) {
      console.error(error);
    } finally {
      // setLoading(false);
    }
  }
    else {
      console.log("URL empty")
    }

  };

//Scanning for XSS =================================

  const scanXss = async () => {
    if (url) {
    console.log("URL ", url)
    try {
    fetch('/scanXss', {
      method: 'POST',
     headers: {
       'Content-Type': 'application/json'
     },
      body: JSON.stringify({ url })
     })
    .then(response => response.json())
    .then(data => {
      console.log('Response - ', data);
      // Process the received data here
      setXssResult(data);
    })
    } catch (error) {
      console.error(error);
    } finally {
      //setLoading(false);
    }
  }
    else {
      console.log("URL empty")
    }

  };


//========== SCAN Network =============

const scanNetwork = async () => {
  if (url) {
  console.log("URL ", url)
  try {
  fetch('/scanNetwork', {
    method: 'POST',
   headers: {
     'Content-Type': 'application/json'
   },
    body: JSON.stringify({ url })
   })
  .then(response => response.json())
  .then(data => {
    console.log('Response - ', data);
    // Process the received data here
    setNetworkResult(data);
  })
  } catch (error) {
    console.error(error);
  } finally {
    //setLoading(false);
  }
}
  else {
    console.log("URL empty")
  }

};


// ============= SQLI ========================
const scanSQLI = async () => {
  if (url) {
  console.log("URL ", url)
  try {
  fetch('/scanSQLI', {
    method: 'POST',
   headers: {
     'Content-Type': 'application/json'
   },
    body: JSON.stringify({ url })
   })
  .then(response => response.json())
  .then(data => {
    console.log('Response - ', data);
    // Process the received data here
    setSqliResult(data.response);
  })
  } catch (error) {
    console.error(error);
  } finally {
    //setLoading(false); 
  }
}
  else {
    console.log("URL empty")
  }

};

 //===========XSS=========
  const printData = (data) => {
    return (
      <div>
        {data ? data : ''}
        </div>
    )
  }

//===========Scan Network=========
useEffect(() => {

  const getServiceName = (port) => {
    switch (port) {
      case '22':
        return 'SSH';
      case '23':
        return 'TELNET';
      case '80':
        return 'HTTP';
      case '443':
        return 'HTTPS';
      // Add more cases for other ports you want to handle
      default:
        return 'Unknown';
    }
  };

  const formatNetworkData = (networkResult) => {
    return Object.entries(networkResult).map(([ipPort, [id, password]]) => {
      const [ip, port] = ipPort.split(":");
      return (
        <List
          sx={{
          width: '100%',
          maxWidth: 360,
          bgcolor: 'background.paper',
        }}
        >
        <ListItem>
        <ListItemAvatar>
          <Avatar>
            <ComputerRoundedIcon />
          </Avatar>
        </ListItemAvatar>
        <Card style={{backgroundColor: "black"}} sx={{ minWidth: 275,color: "white" }} >
      <CardContent>
        <Typography>
          IP scanned - {ip} 
        </Typography>
        <Typography>
          Service Attacked - {getServiceName(port)}  - {port}
        </Typography>
        <Typography style={{backgroundColor: "green"}}>
          Credentials
          <br />
          Username - {id} and Password - {password}
        </Typography>
      </CardContent>
    </Card>
        <ListItemText />
      </ListItem>
      <Divider variant="inset" component="li" />
        
        
        </List>
      );
    });
  };
      

  if(Object.keys(networkResult).length > 0 ){
    console.log(networkResult)
    const data = formatNetworkData(networkResult)
    // setNetworkData(data)
    setNetworkData(data)
    setTestingNetwork(true)
}else{
  setTestingNetwork(false)
}
},[networkResult])
  

//=============== SQLI Set Data ================

useEffect(() => {

 
  const formatSqliData = (sqliResult) => {
    return(
      <div>
    {sqliResult && (
      <div>
        {Array.isArray(sqliResult) ? (
          <div>
            SQLI Found in following url - 
          <ul>
            {sqliResult.map((item, index) => (
              <li key={index}>{item}</li>
            ))}
          </ul>
          </div>
        ) : (
          <p>{sqliResult}</p>
        )}
      </div>
    )}
  </div>
    )
  };
      
  if(Object.keys(sqliResult).length > 0 ){
    console.log(sqliResult)
    const data = formatSqliData(sqliResult)
    // setNetworkData(data)
    setSqliData(data)
    setTestingSqli(true)
}else{
  setTestingSqli(false)
}
},[sqliResult])

  //===========XSS=========
  useEffect(() => {

    const forMatXssData = () => {
   
      const inputs = xssResult?.response[1]?.inputs;
    
      return (
        <div>
        {xssResult?.response ?
        <div>
            <div> {xssResult?.response[1] && inputs ? xssResult.response[0] : xssResult.response }</div>

            <div>{xssResult?.response[1] && inputs ?
              <div className="action">
                
                <p>Action: {xssResult.response[1].action}</p>
                <p>Method: {xssResult.response[1].method}</p>
                {inputs.map((input, index) => (
                  <ul className="input" key={index}>
                    <li>Name: {input.name}</li>
                    <li>Type: {input.type}</li>
                    <li>Value: {input.value}</li>
                  </ul>
                ))}
              </div>
            : ''
          }
          </div>

        </div>
          : ''
          }
        </div>
      );
      }

    if(Object.keys(xssResult).length > 0 && xssResult.response){
      const data=forMatXssData(xssResult)
      setXssData(data)
      setTestingXss(true)
  }else{
    setTestingXss(false)
  }
  },[xssResult])


//=========WebTech===============
useEffect(() => {

  const formatUrlChgeckData = (urlCheckResult) => {
    return (
      <div>
        {Object.keys(urlCheckResult).map((key) => (
        <div key={key}>
          <p>Software Version: {urlCheckResult[key].softwareversion}</p>
          <h3>Vulnerability: {key}</h3>
          <p>CVE Score: {urlCheckResult[key].cvescore}</p>
          <p>Link: <a href={urlCheckResult[key].href}>{urlCheckResult[key].href}</a></p>
          
          {/* Include additional fields as needed */}
        </div>
      ))}
      </div>
    )
  }

  if(Object.keys(urlCheckResult).length > 0){
    const data=formatUrlChgeckData(urlCheckResult)
    setWebTechData(data)
    setTestingWebTech(true)
}else{
  setTestingWebTech(true)
  setWebTechData('No vulnerabilities found.')
}
},[urlCheckResult])


//==========Cleaning Data ===========
  function cleanData(){
    setTestingXss(false)
    setTestingSqli(false)
    setTestingWebTech(false)
    setTestingNetwork(false)
    setXssData()
    setWebTechData()
    setSqliData()
    setNetworkData()
  }

  //===========Button Action=========
  const handleButtonClick = (buttonName) => {
    setActiveButton(buttonName);
    cleanData()
    
    // Perform the desired action based on the button clicked
    switch (buttonName) {
      case 'xss':
        // Perform XSS scanning
        setTestingXss(true)
        scanXss();
        break;
      case 'sql':
        // Perform SQL scanning
        setTestingSqli(true)
        scanSQLI()
        break;
      case 'webTech':
        // Perform web technology scanning
        setTestingWebTech(true)
        scanWebsiteTech();
        break;
      case 'network':
        setTestingNetwork(true)
        scanNetwork();
        // Perform network scanning
        break;
      default:
        break;
    }
  };


  return (
    <div>
    <div className={classes.root}>
      <TextField
        className={classes.inputField}
        label="Enter URL"
        variant="outlined"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <div className={classes.buttonContainer}>
        <Button
          className={`${classes.scanButton} ${activeButton === 'xss' && classes.activeButton}`}
          variant="contained"
          onClick={() => handleButtonClick('xss')}
        >
          Scan For XSS
        </Button>
        <Button
          className={`${classes.scanButton} ${activeButton === 'sql' && classes.activeButton}`}
          variant="contained"
          onClick={() => handleButtonClick('sql')}
        >
          Scan for SQL
        </Button>
        <Button
          className={`${classes.scanButton} ${activeButton === 'webTech' && classes.activeButton}`}
          variant="contained"
          onClick={() => handleButtonClick('webTech')}
        >
          Scan Web Technologies
        </Button>
        <Button
          className={`${classes.scanButton} ${activeButton === 'network' && classes.activeButton}`}
          variant="contained"
          onClick={() => handleButtonClick('network')}
        >
          Scan Network
        </Button>
      </div>
      <Container maxWidth="md" className={classes.dataContainer}>
      {(testingXss || testingSqli || testingWebTech || testingNetwork) && (
    <>
        {testingXss ?  printData(xssData ? xssData : "Scanning for XSS ... Please Wait") : ''}
        {testingSqli ? printData(sqliData ? sqliData : "Scanning for SQL Injection ... Please Wait") : ''}
        {testingWebTech ? printData(webTechData ? webTechData : "Scanning Web Technologies ... Please Wait") : ''}
        {testingNetwork ? printData(networkData ? networkData : "Scanning Network ... Pelase Wait") : ''}
    </>
        )}
      </Container>
    </div>
    </div>
  );
}
    

export default App;

