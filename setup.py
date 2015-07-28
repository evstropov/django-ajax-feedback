from setuptools import setup

setup(
    name='django-ajaxfeedback',
    version=__import__('ajax_feedback').__version__,
    description='Django easy ajax feedback form.',
    author='Evstropov Nikita',
    author_email='evstropov.n@gmail.com',
    url='https://github.com/evstropov/django-ajax-feedback',
    packages=['ajax_feedback'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 2.7",
        'Framework :: Django',
    ],
    include_package_data=True,
    zip_safe=False,
)
