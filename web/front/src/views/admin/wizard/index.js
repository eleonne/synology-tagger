import React, {useEffect, useState} from "react"
import {
    Box,
    Link,
    Flex,
    Spinner,
    Text,
    HStack,
    RadioGroup,
    Radio,
    FormControl,
    FormLabel,
    Input,
    Button,
    Icon,
} from "@chakra-ui/react";
import {
    MdCloudDone,
    MdCloudOff,
    MdFolderOpen,
    MdFolderOff
} from "react-icons/md";
import {
    BsDatabaseFillCheck,
    BsDatabaseFillSlash,
} from "react-icons/bs";
import { Cron } from 'react-js-cron'
import 'react-js-cron/dist/styles.css'
import { ExternalLinkIcon } from '@chakra-ui/icons'
import Card from '../../../components/card/Card'
import { VSeparator } from "../../../components/separator/Separator";
import IconBox from "../../../components/icons/IconBox";
import axios from "axios"

export default function UserReports() {

    const [state, setState] = useState({
        "data": {
            "DEVICE": "gpu",
            "MEDIA_FOLDER": "/media/nas",
            "CRONTAB": "* * * * *",
            "MYSQL_PASSWORD": "",
            "MYSQL_USER": "",
            "PG_PASSWORD": "",
            "PG_USERNAME": "",
            "SSH_PASSWORD": "",
            "SSH_PORT": "",
            "SSH_USERNAME": "",
            "SYNOLOGY_HOST": "",
            "THRESHOLD": "0.4",
            "VIDEO_THRESHOLD": "0.6",
        },
        "ssh": {
            "is_connected": "false",
            "error_message": "",
        },
        "postgres": {
            "is_connected": "false",
            "error_message": "",
        },
        "media_folder": {
            "is_connected": "false",
            "error_message": ""
        },
        "isLoading": 'false',
    })

    useEffect(() => {
        async function fetchData() {
            const [config, ssh, postgres, media_folder] = await Promise.all([
                axios.get(process.env.REACT_APP_API_URL + '/get-config'),
                axios.get(process.env.REACT_APP_API_URL + '/test-ssh'),
                axios.get(process.env.REACT_APP_API_URL + '/test-postgres'),
                axios.get(process.env.REACT_APP_API_URL + '/test-media-folder')
            ])
            setState({
                ...state,
                isLoading: 'false',
                data: {...config.data},
                ssh: {...ssh.data},
                postgres: {...postgres.data},
                media_folder: {...media_folder.data}
            })
        }
        setState({
            ...state,
            isLoading: 'true',
        })
        fetchData()
    }, [])

    const getTitle = (title) => (
        <Flex
            align={{ sm: "flex-start", lg: "center" }}
            justify='space-between'
            w='100%'
            px='22px'
            mb='10px'
            boxShadow='0px 40px 58px -20px rgba(112, 144, 176, 0.26)'
            >
            <Text fontSize='xl' fontWeight='600'>
                {title} {state.isLoading == 'true' ? <Spinner /> : null}
            </Text>
        </Flex>
    )

    const getField = (label, type, stateKey, placeholder = '', disabled = false) => {
        
        let is_disabled = false
        if (disabled == true)
            is_disabled = true
        else
            is_disabled = state.isLoading == 'true'

        return (<Box display="flex" flexDir='column' w='100%'>
            <FormLabel
                display='flex'
                ms='4px'
                fontSize='sm'
                fontWeight='800'
                mb='8px'>
            {label}
            </FormLabel>
            <Input
                isRequired={true}
                // variant='auth'
                fontSize='sm'
                disabled={is_disabled}
                ms={{ base: "0px", md: "0px" }}
                type={type}
                placeholder={placeholder}
                mb='24px'
                fontWeight='500'
                size='lg'
                value={state['data'][stateKey]}
                onChange={handle}
                name={stateKey}
            />
        </Box>)
    }

    const saveHandler = () => {
        setState({
            ...state,
            isLoading: 'true'
        })
        axios.post(process.env.REACT_APP_API_URL + '/save-config', state['data']).then((response) => {
            setState({
                ...state,
                isLoading: 'false'
            })
        })
    }

    const testSSHHandler = () => {
        setState({
            ...state,
            isLoading: 'true'
        })
        axios.post(process.env.REACT_APP_API_URL + '/save-config', state['data']).then((response) => {
            axios.get(process.env.REACT_APP_API_URL + '/test-ssh').then((response) => {
                setState({
                    ...state,
                    isLoading: 'false',
                    ssh: {...response.data}
                })
            })
        })
    }

    const testPostgresHandler = () => {
        setState({
            ...state,
            isLoading: 'true'
        })
        axios.post(process.env.REACT_APP_API_URL + '/save-config', state['data']).then((response) => {
            axios.get(process.env.REACT_APP_API_URL + '/test-postgres').then((response) => {
                setState({
                    ...state,
                    isLoading: 'false',
                    postgres: {...response.data}
                })
            })
        })
    }

    const createConnectionHandler = () => {
        setState({
            ...state,
            isLoading: 'true'
        })
        axios.post(process.env.REACT_APP_API_URL + '/save-config', state['data']).then((response) => {
            axios.get(process.env.REACT_APP_API_URL + '/create-postgres-connection').then((response) => {
                setState({
                    ...state,
                    isLoading: 'false',
                    postgres: {
                        "is_connected": 'true',
                        "error_message": response.data.stdout,
                    }
                })
            })
        })
    }

    const testMediaFolderHandler = () => {
        setState({
            ...state,
            isLoading: 'true'
        })
        axios.post(process.env.REACT_APP_API_URL + '/save-config', state['data']).then((response) => {
            axios.get(process.env.REACT_APP_API_URL + '/test-media-folder').then((response) => {
                setState({
                    ...state,
                    isLoading: 'false',
                    media_folder: {...response.data}
                })
            })
        })
    }

    const setCron = (cron) => {
        const data = {...state}
        data.data['CRONTAB'] = cron
        setState({
            ...data
        })
    }

    const handle = ({target}) => {
        const v = {
            ...state
        }
        v['data'][target.name] = target.value

        setState({
            ...v
        })
    }

    return (
        <>
            <Button disabled={state.isLoading == 'true'} onClick={saveHandler} colorScheme='blue' size='lg'>Save</Button>
            
            <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
                {getTitle('Synology')}
                <Card>
                    <FormControl>
                        {getField('Host', 'text', 'SYNOLOGY_HOST', 'Eg. 192.168.1.1')}
                        <Box display="flex" flexDirection='row'>
                            <Button onClick={testSSHHandler} disabled={state.isLoading == 'true'} colorScheme='blue' size='sm'>Test SSH Connection</Button>
                            <VSeparator w='24px' bg='white' />
                            {
                                state.ssh.is_connected == 'true' ? 
                                    <>
                                        <IconBox
                                            w='24px'
                                            h='24px'
                                            // bg={boxBg}
                                            icon={
                                                <Icon w='24px' h='24px' as={MdCloudDone} color='green'/>
                                            }/>
                                        <Text color='green'>Connected</Text>
                                    </>
                                    :
                                    <>
                                        <IconBox
                                            w='24px'
                                            h='24px'
                                            // bg={boxBg}
                                            icon={
                                                <Icon w='24px' h='24px' as={MdCloudOff} color='red'/>
                                            }/>
                                        <Text color='red'>Not Connected: {state.ssh.error_message}</Text>
                                    </>
                            }
                        </Box>
                        <Box display="flex" flexDirection='row'>
                            {getField('Username', 'text', 'SSH_USERNAME')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Password', 'text', 'SSH_PASSWORD')}
                            <VSeparator w='24px' bg='white' />
                            {getField('port', 'text', 'SSH_PORT')}
                        </Box>
                        <Box display="flex" flexDirection='row'>
                            <Button disabled={state.ssh.is_connected == 'false' || state.isLoading == 'true'} onClick={testPostgresHandler} colorScheme='blue' size='sm'>Test Postgres Connection</Button>
                            <VSeparator w='24px' bg='white' />
                            <Button disabled={state.ssh.is_connected == 'false' || state.isLoading == 'true'} onClick={createConnectionHandler} colorScheme='blue' size='sm'>Create Postgres Connection</Button>
                            <VSeparator w='24px' bg='white' />
                            {
                                state.postgres.is_connected == 'true' ? 
                                    <>
                                        <IconBox
                                            w='24px'
                                            h='24px'
                                            // bg={boxBg}
                                            icon={
                                                <Icon w='24px' h='24px' as={BsDatabaseFillCheck} color='green'/>
                                            }/>
                                        <Text color='green'>Connected</Text>
                                    </>
                                    :
                                    <>
                                        <IconBox
                                            w='24px'
                                            h='24px'
                                            // bg={boxBg}
                                            icon={
                                                <Icon w='24px' h='24px' as={BsDatabaseFillSlash} color='red'/>
                                            }/>
                                        <Text color='red'>Not Connected: {state.postgres.error_message}</Text>
                                    </>
                            }
                        </Box>
                        <Box display="flex" flexDirection='row'>
                            {getField('Username', 'text', 'PG_USERNAME')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Password', 'text', 'PG_PASSWORD')}
                        </Box>
                    </FormControl>
                </Card>
            </Box>

            <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
                {getTitle('Local')}
                <Card>
                    <FormControl>
                        <Box display="flex" flexDirection='row'>
                            <Button disabled={state.isLoading == 'true' || state.postgres.is_connected == 'false'} onClick={testMediaFolderHandler} colorScheme='blue' size='sm'>
                                Test Folder
                            </Button>
                            <VSeparator w='24px' bg='white' />
                            {
                                state.media_folder.is_connected == 'true' ? 
                                    <>
                                        <IconBox
                                            w='24px'
                                            h='24px'
                                            // bg={boxBg}
                                            icon={
                                                <Icon w='24px' h='24px' as={MdFolderOpen} color='green'/>
                                            }/>
                                        <Text color='green'>Connected</Text>
                                    </>
                                    :
                                    <>
                                        <IconBox
                                            w='24px'
                                            h='24px'
                                            // bg={boxBg}
                                            icon={
                                                <Icon w='24px' h='24px' as={MdFolderOff} color='red'/>
                                            }/>
                                        <Text color='red'>Not Connected: {state.media_folder.error_message}</Text>
                                    </>
                            }
                        </Box>
                        <Box display="flex" flexDirection='row'>
                            {getField('Media Folder', 'text', 'MEDIA_FOLDER', 'Eg. /media/xxx/yyyy', true)}
                            <VSeparator w='24px' bg='white' />
                            <Box display="flex" flexDirection='column'>
                                <Text fontWeight='500' >Compute Using:</Text>
                                <RadioGroup defaultValue='gpu'>
                                    <HStack spacing='24px'>
                                        <Radio checked={state.DEVICE == 'gpu'} value='gpu'>GPU</Radio>
                                        <Radio checked={state.DEVICE == 'cpu'} value='cpu'>CPU</Radio>
                                    </HStack>
                                </RadioGroup>
                            </Box> 
                        </Box> 
                        <Text >Certainty to Classify (only classifications with certainty higher than the percentage specified will be considered)</Text>
                        <Box display="flex" flexDirection='row'>
                            {getField('Images', 'text', 'THRESHOLD', 'Eg. 40')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Videos', 'text', 'VIDEO_THRESHOLD', 'Eg. 60')}
                        </Box> 
                    </FormControl>
                </Card>
            </Box>

            <Box pt={{ base: "130px", md: "80px", xl: "80px" }}>
                {getTitle('Scheduling')}
                <Card>
                    <Cron value={state.data.CRONTAB} setValue={setCron} />
                </Card>
            </Box>
            <Button onClick={saveHandler} colorScheme='blue' size='lg'>Save</Button>
        </>
    )
}