import { Fragment } from 'react'
import './index.css'
import { HeaderProps } from './types'

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function Header({ handleTestCode, handleSubmit }: HeaderProps) {
  return (
    <div className="lg:flex lg:items-center lg:justify-between border border-gray-200 p-10">
      <div className="min-w-0 flex-1">
        <h2 className="heading text-2xl font-bold leading-7 sm:truncate sm:text-3xl sm:tracking-tight">
          Datacurve Python Sandbox
        </h2>
      </div>
      <div className="mt-5 flex lg:ml-4 lg:mt-0">
        <span className="ml-3 hidden sm:block">
          <button
            type="button"
            className="btn inline-flex items-center rounded-md px-3 py-2 text-sm font-semibold shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50" 
            onClick={handleTestCode}
          >
            Test Code
          </button>
        </span>

        <span className="sm:ml-3">
          <button
            type="button"
            className="btn inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            onClick={handleSubmit}
          >
            Submit
          </button>
        </span>
      </div>
    </div>
  )
}
