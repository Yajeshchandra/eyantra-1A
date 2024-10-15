from setuptools import setup

package_name = 'wd_task_1a'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=[
        'wd_task_1a.task_1a_3402'
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='your_name',
    maintainer_email='your_email@example.com',
    description='Turtlesim drone drawing simulation',
    license='Your License',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'task_1a_3402 = wd_task_1a.task_1a_3402:main',
        ],
    },
)
