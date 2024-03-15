import Loading from './Loading'
import { Suspense } from 'react'
import { Outlet } from 'react-router-dom'

const Root = () => {

    return (
        <Suspense fallback={<Loading loading={true} />}>
            <Outlet />
        </Suspense>
    )
}

export default Root
