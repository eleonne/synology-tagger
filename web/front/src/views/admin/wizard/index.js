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
} from "react-icons/md";
import { ExternalLinkIcon } from '@chakra-ui/icons'
import Card from '../../../components/card/Card'
import { VSeparator } from "../../../components/separator/Separator";
import IconBox from "../../../components/icons/IconBox";
import axios from "axios"

export default function UserReports() {

    const [state, setState] = useState({
        "data": {
            "DAY_OF_MONTH": "*",
            "DAY_OF_WEEK": "*",
            "DEVICE": "gpu",
            "HOUR": "0",
            "MEDIA_FOLDER": "/media/nas",
            "MINUTE": "0",
            "MONTH": "*",
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
        "isLoading": 'false',
    })

    useEffect(() => {
        setState({
            ...state,
            isLoading: 'true'
        })
        axios.get(process.env.REACT_APP_API_URL + '/get-config').then((response) => {
            setState({
                ...state,
                data: {...response.data},
                isLoading: 'false'
            })
        })
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

    const getField = (label, type, stateKey, placeholder = '') => (
        <Box display="flex" flexDir='column' w='100%'>
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
                disabled={state.isLoading == 'true'}
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
        </Box>
    )

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
                    ssh: {
                        "is_connected": response.data.connected,
                        "error_message": response.data.error_msg,
                    }
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
                    postgres: {
                        "is_connected": response.data.connected,
                        "error_message": response.data.error_msg,
                    }
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
                            {getField('Media Folder', 'text', 'MEDIA_FOLDER', 'Eg. /media/xxx/yyyy')}
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
                    <FormControl>
                        <Text >This is a CRONTAB config. You can check this <Link href="https://crontab.guru/" isExternal>site<ExternalLinkIcon mx='2px' /></Link> to understand the logic</Text>
                        <Box display="flex" flexDirection='row'>
                            {getField('Minute', 'text', 'MINUTE', 'Eg. *')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Hour', 'text', 'HOUR', 'Eg. *')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Day of the Month', 'text', 'DAY_OF_MONTH', 'Eg. *')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Month', 'text', 'MONTH', 'Eg. *')}
                            <VSeparator w='24px' bg='white' />
                            {getField('Day of the Week', 'text', 'DAY_OF_WEEK', 'Eg. *')}
                        </Box> 
                    </FormControl>
                </Card>
            </Box>
            {state.error_message ? <Text color='red'>{state.error_message}</Text> : null}
            {state.success_message ? <Text color='green'>{state.success_message}</Text> : null}
            <Button onClick={saveHandler} colorScheme='blue' size='lg'>Save</Button>
        </>
    )
}